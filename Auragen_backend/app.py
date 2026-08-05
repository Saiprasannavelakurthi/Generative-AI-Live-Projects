from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from generator import generator
from websocket_manager import manager

from routes.generate import router as generate_router

from services.cognitive_engine import cognitive_engine
from services.generation_controller import generation_controller
from utils.validator import validate_component
from utils.security_validator import validate_security
from utils.save_code import save_component
from utils.logger import logger


app = FastAPI(
    title="AuraGen AI Backend",
    version="1.0.0",
    description="AI Backend for generating React components using Groq + LangChain",
)

# ==========================================================
# CORS
# ==========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change in production
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
    }


# ==========================================================
# WebSocket
# ==========================================================

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    await manager.connect(websocket)

    logger.info("Frontend connected.")

    try:

        while True:

            data = await websocket.receive_json()

            print("\n========== RECEIVED ==========")
            print(data)
            print("==============================")

            result = cognitive_engine.calculate_score(
                data.get("events", [])
            )

            print("Cognitive:", result)

            logger.info(f"Received telemetry: {data}")

            if data.get("type") != "telemetry_batch":

                await manager.send_json(
                    websocket,
                    {
                        "status": "received"
                    }
                )

                continue

            # ----------------------------------------
            # Cognitive score
            # ----------------------------------------

            result = cognitive_engine.calculate_score(
                data.get("events", [])
            )

            logger.info(
                f"Cognitive Result: {result}"
            )

            # ----------------------------------------
            # Send score
            # ----------------------------------------

            await manager.send_json(
                websocket,
                {
                    "type": "cognitive_score",
                    "score": result["score"],
                    "high_load": result["high_load"],
                },
            )

            should_generate = (
                    result["high_load"]
                    or data.get("user_action") in [
                        "move",
                        "click",
                        "hesitation"
                    ]
            )

            logger.info(
                f"Should Generate: {should_generate}"
            )

            if not should_generate:
                logger.info("Skipping UI generation")
                continue

            allowed = generation_controller.can_generate()
            print("Generation Controller:", allowed)

            if not allowed:
                logger.info("Generation skipped (cooldown)")
                continue

            logger.info("Generating Adaptive UI...")

            full_code = ""

            try:
                print("========== START GENERATION ==========")
                for token in generator.stream_component(
                        user_prompt="Generate Adaptive UI",
                        dom_state=data.get("dom_state", ""),
                        form_data=data.get("form_data", {}),
                        session_id=data.get("session_id", ""),
                        page_name=data.get("page_name", ""),
                        current_component=data.get("current_component", ""),
                        active_field=data.get("active_field", ""),
                        cognitive_score=result["score"],
                        user_action=data.get("user_action", ""),
                ):
                    full_code += token

                    await manager.send_json(
                        websocket,
                        {
                            "type": "token",
                            "content": token,
                        },
                    )
                print("========== END GENERATION ==========")

                status, message = validate_component(
                    full_code
                )

                if not status:
                    logger.warning(
                        f"Validation failed: {message}"
                    )

                    await manager.send_json(
                        websocket,
                        {
                            "type": "error",
                            "message": message,
                        },
                    )

                    continue

                safe, security_message = validate_security(
                    full_code
                )

                if not safe:
                    logger.warning(
                        f"Security validation failed: "
                        f"{security_message}"
                    )

                    await manager.send_json(
                        websocket,
                        {
                            "type": "error",
                            "message": security_message,
                        },
                    )

                    continue

                filename = (
                        data.get("page_name", "").title().replace(" ", "")
                        or "GeneratedComponent"
                )

                saved_filename = save_component(
                    filename,
                    full_code
                )

                logger.info(
                    f"Component saved: {saved_filename}"
                )

                await manager.send_json(
                    websocket,
                    {
                        "type": "complete",
                        "filename": saved_filename,
                        "generated_code": full_code,
                        "page_name": data.get("page_name", ""),
                        "session_id": data.get("session_id", ""),
                        "preserved_data": True,
                        "context_version": 3,
                    },
                )

            except Exception:

                logger.exception(
                    "Streaming generation failed."
                )

                await manager.send_json(
                    websocket,
                    {
                        "type": "error",
                        "message": "Component generation failed.",
                    },
                )

    except WebSocketDisconnect:

        manager.disconnect(websocket)

        logger.info("Frontend disconnected.")