from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import time

from generator import generator
from websocket_manager import manager

from routes.generate import router as generate_router

from services.cognitive_engine import cognitive_engine
from services.generation_controller import generation_controller

from utils.validator import validate_component
from utils.security_validator import validate_security
from utils.save_code import save_component
from utils.logger import logger

# ==========================================================
# FastAPI Application
# ==========================================================

app = FastAPI(
    title="AuraGen AI Backend",
    version="1.0.0",
    description="Adaptive React UI Generator using Groq + LangChain",
)

# ==========================================================
# CORS
# ==========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # Change in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================================
# Routes
# ==========================================================

app.include_router(generate_router)

# ==========================================================
# Health APIs
# ==========================================================

@app.get("/")
def home():
    return {
        "project": "AuraGen",
        "status": "Running",
        "version": "1.0.0",
    }


@app.get("/health")
def health():
    return {
        "status": "Healthy",
        "websocket_clients": len(manager.active_connections),
    }


# ==========================================================
# WebSocket
# ==========================================================

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    await manager.connect(websocket)

    logger.info("Frontend connected.")
    logger.info(
        f"Active Connections: {len(manager.active_connections)}"
    )

    try:

        while True:

            data = await websocket.receive_json()

            logger.info(
                "========== TELEMETRY RECEIVED =========="
            )
            logger.info(data)

            # Ignore invalid payloads
            if data.get("type") != "telemetry_batch":

                await manager.send_json(
                    websocket,
                    {
                        "status": "received"
                    }
                )

                continue

            # -----------------------------------------
            # Calculate Cognitive Score
            # -----------------------------------------

            result = cognitive_engine.calculate_score(
                data.get("events", [])
            )

            logger.info(
                f"Cognitive Score: {result}"
            )

            # Send score immediately to frontend

            await manager.send_json(
                websocket,
                {
                    "type": "cognitive_score",
                    "score": result["score"],
                    "high_load": result["high_load"],
                },
            )
            logger.info("✅ Sent cognitive_score")

            # Decide whether a new UI should be generated

            should_generate = (
                result["high_load"]
                or data.get("user_action") in [
                    "move",
                    "click",
                    "hesitation",
                ]
            )

            logger.info(
                f"Should Generate: {should_generate}"
            )

            if not should_generate:
                continue

            allowed = generation_controller.can_generate(
                data.get("session_id", "default")
            )
            logger.info(
                f"Generation Allowed: {allowed}"
            )

            if not allowed:
                continue

            start_time = time.perf_counter()

            full_code = ""

            try:

                logger.info("========== START GENERATION ==========")

                prompt = (
                    f"Generate an adaptive React UI for "
                    f"{data.get('page_name', 'login')} page "
                    f"based on the current DOM, "
                    f"user interaction and cognitive score."
                )
                logger.info("Before stream_component()")
                for token in generator.stream_component(
                        user_prompt=prompt,
                        dom_state=data.get("dom_state", ""),
                        form_data=data.get("form_data", {}),
                        session_id=data.get("session_id", ""),
                        page_name=data.get("page_name", ""),
                        current_component=data.get("current_component", ""),
                        active_field=data.get("active_field", ""),
                        cognitive_score=result["score"],
                        user_action=data.get("user_action", ""),
                ):
                    logger.info(f"TOKEN FROM GENERATOR: {repr(token)}")
                    full_code += token
                    await manager.send_json(
                        websocket,
                        {
                            "type": "token",
                            "content": token,
                        },
                    )
                    logger.info("Token sent to frontend")
                logger.info("Exited stream_component()")
                logger.info(f"Total code length: {len(full_code)}")
                logger.info("========== END GENERATION ==========")

                logger.info("Generated Component Successfully")

                import re

                if not re.search(
                        r"const\s+Component\s*=\s*\(\s*\)\s*=>",
                        full_code,
                ):
                    full_code = f"""const Component = () => {{
                    return (
                {full_code}
                    );
                }};"""

                # -----------------------------------------
                # Validate Generated Component
                # -----------------------------------------

                status, message = validate_component(full_code)

                logger.info(message)

                if not status:
                    await manager.send_json(
                        websocket,
                        {
                            "type": "error",
                            "message": message,
                        },
                    )

                    continue

                # -----------------------------------------
                # Security Validation
                # -----------------------------------------

                safe, security_message = validate_security(full_code)

                logger.info(security_message)

                if not safe:
                    await manager.send_json(
                        websocket,
                        {
                            "type": "error",
                            "message": security_message,
                        },
                    )

                    continue

                # -----------------------------------------
                # Save Component
                # -----------------------------------------

                filename = (
                    data.get(
                        "page_name",
                        "GeneratedComponent"
                    )
                    .replace(" ", "")
                    .replace("/", "")
                    .replace("\\", "")
                )

                saved_filename = save_component(
                    filename,
                    full_code,
                )

                logger.info(
                    f"Component Saved: {saved_filename}"
                )

                elapsed = round(
                    time.perf_counter() - start_time,
                    2,
                )

                logger.info(
                    f"Generation completed in {elapsed} sec"
                )

                # -----------------------------------------
                # Send Final Component
                # -----------------------------------------

                await manager.send_json(
                    websocket,
                    {
                        "type": "complete",
                        "filename": saved_filename,
                        "generated_code": full_code,
                        "generation_time": elapsed,
                        "page_name": data.get(
                            "page_name",
                            "",
                        ),
                        "session_id": data.get(
                            "session_id",
                            "",
                        ),
                        "preserved_data": True,
                        "context_version": 3,
                    },
                )

                logger.info("✅ Complete message sent")
                logger.info(f"Generated code length: {len(full_code)}")

            except Exception as e:

                logger.exception(
                    "Component generation failed."
                )

                await manager.send_json(
                    websocket,
                    {
                        "type": "error",
                        "message": str(e),
                    },
                )

    except WebSocketDisconnect:

        manager.disconnect(websocket)

        logger.info("Frontend disconnected.")

        logger.info(
            f"Active Connections: {len(manager.active_connections)}"
        )

    except Exception:

        logger.exception(
            "Unexpected WebSocket error."
        )

        try:
            await manager.send_json(
                websocket,
                {
                    "type": "error",
                    "message": "Internal Server Error",
                },
            )
        except Exception:
            pass

        manager.disconnect(websocket)

        logger.info(
            f"Active Connections: {len(manager.active_connections)}"
        )