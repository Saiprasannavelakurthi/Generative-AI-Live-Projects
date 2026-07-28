from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from generator import generator
from websocket_manager import manager

from services.cognitive_engine import cognitive_engine
from services.decision_engine import decision_engine
from services.prompt_builder import prompt_builder

from utils.validator import validate_component
from utils.security_validator import validate_security
from utils.save_code import save_component
from utils.logger import logger

from routes.generate import router as generate_router


# =========================================================
# FastAPI Application
# =========================================================

app = FastAPI(
    title="AuraGen AI Backend",
    version="1.0.0",
    description="AI Backend for generating React components using Groq + LangChain"
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # Restrict this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# Routes
# =========================================================

app.include_router(generate_router)


@app.get("/")
def home():
    return {
        "project": "AuraGen",
        "status": "Running",
        "version": "1.0.0"
    }


@app.get("/health")
def health():
    return {
        "status": "Healthy"
    }


# =========================================================
# WebSocket
# =========================================================

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    await manager.connect(websocket)

    print("Frontend Connected")

    # Remember the last UI sent to this connection.
    # This prevents generating the same UI repeatedly.
    last_ui_type = None

    try:

        while True:

            # ---------------------------------------------------------
            # Receive frontend telemetry
            # ---------------------------------------------------------

            data = await websocket.receive_json()

            print("Received:", data)

            # Ignore messages that are not telemetry batches
            if data.get("type") != "telemetry_batch":
                continue

            events = data.get("events", [])

            # ---------------------------------------------------------
            # Cognitive analysis
            # ---------------------------------------------------------

            try:

                result = cognitive_engine.calculate_score(events)

            except Exception:

                logger.exception(
                    "Cognitive score calculation failed"
                )

                await manager.send_json(
                    websocket,
                    {
                        "type": "generation_error",
                        "message": "Unable to analyse telemetry."
                    }
                )

                continue

            print("Cognitive Result:", result)

            score = result["score"]
            high_load = result["high_load"]


            # ---------------------------------------------------------
            # Decide which UI should be displayed
            # ---------------------------------------------------------

            try:

                ui_type = decision_engine.decide_ui(score)

            except Exception:

                logger.exception(
                    "UI decision failed"
                )

                await manager.send_json(
                    websocket,
                    {
                        "type": "generation_error",
                        "message": "Unable to select UI."
                    }
                )

                continue

            print("Selected UI:", ui_type)


            # ---------------------------------------------------------
            # Send cognitive information to frontend
            # ---------------------------------------------------------

            await manager.send_json(
                websocket,
                {
                    "type": "cognitive_score",
                    "score": score,
                    "high_load": high_load,
                    "ui_type": ui_type
                }
            )


            # ---------------------------------------------------------
            # Don't regenerate the same UI
            # ---------------------------------------------------------

            if ui_type == last_ui_type:

                print(
                    "UI unchanged:",
                    ui_type,
                    "- skipping generation"
                )

                continue


            print(
                f"UI CHANGE: {last_ui_type} -> {ui_type}"
            )


            # ---------------------------------------------------------
            # Build prompt
            # ---------------------------------------------------------

            try:

                prompt = prompt_builder.build_prompt(ui_type)

            except Exception:

                logger.exception(
                    "Prompt building failed"
                )

                await manager.send_json(
                    websocket,
                    {
                        "type": "generation_error",
                        "message": "Unable to build UI prompt."
                    }
                )

                continue

            print("Prompt:", prompt)


            # ---------------------------------------------------------
            # Generate React component
            # ---------------------------------------------------------

            try:

                print(">>> STARTING GENERATOR")

                generated = generator.generate_component(
                    user_prompt=prompt
                )

                print(">>> GENERATOR RETURNED")
                print(">>> RESULT:", generated)

                generated_code = generated["generated_code"]
                filename = generated["filename"]

                print("Generated:", filename)

            except Exception as e:

                print(">>> GENERATOR ERROR:", repr(e))

                logger.exception(
                    "WebSocket component generation failed"
                )

                await manager.send_json(
                    websocket,
                    {
                        "type": "generation_error",
                        "message": str(e)
                    }
                )

                continue

                generated_code = generated["generated_code"]
                filename = generated["filename"]

                print("Generated:", filename)

                logger.info(
                    f"WebSocket component generated: {filename}"
                )

            except Exception:

                logger.exception(
                    "WebSocket component generation failed"
                )

                await manager.send_json(
                    websocket,
                    {
                        "type": "generation_error",
                        "message": "Component generation failed."
                    }
                )

                continue


            # ---------------------------------------------------------
            # React + Babel validation
            # ---------------------------------------------------------

            valid, validation_message = validate_component(
                generated_code
            )

            if not valid:

                print(
                    "VALIDATION FAILED:",
                    validation_message
                )

                logger.warning(
                    f"WebSocket validation failed: "
                    f"{validation_message}"
                )

                await manager.send_json(
                    websocket,
                    {
                        "type": "generation_error",
                        "message": validation_message
                    }
                )

                continue


            print("Validation passed")


            # ---------------------------------------------------------
            # Security validation
            # ---------------------------------------------------------

            safe, security_message = validate_security(
                generated_code
            )

            if not safe:

                print(
                    "SECURITY FAILED:",
                    security_message
                )

                logger.warning(
                    f"WebSocket security validation failed: "
                    f"{security_message}"
                )

                await manager.send_json(
                    websocket,
                    {
                        "type": "generation_error",
                        "message": security_message
                    }
                )

                continue


            print("Security validation passed")


            # ---------------------------------------------------------
            # Save validated component
            # ---------------------------------------------------------

            try:

                saved_filename = save_component(
                    filename,
                    generated_code
                )

                print(
                    "Component saved:",
                    saved_filename
                )

            except Exception:

                logger.exception(
                    "Unable to save WebSocket component"
                )

                await manager.send_json(
                    websocket,
                    {
                        "type": "generation_error",
                        "message": "Unable to save generated component."
                    }
                )

                continue


            # ---------------------------------------------------------
            # Send component to frontend
            # ---------------------------------------------------------

            print(
                "SENDING COMPONENT TO FRONTEND:",
                saved_filename
            )

            try:

                await manager.send_json(
                    websocket,
                    {
                        "type": "generated_component",
                        "filename": saved_filename,
                        "code": generated_code,
                        "ui_type": ui_type
                    }
                )

            except Exception:

                logger.exception(
                    "Unable to send component to frontend"
                )

                continue


            logger.info(
                f"WebSocket component sent: {saved_filename}"
            )

            print(
                "COMPONENT SENT SUCCESSFULLY:",
                saved_filename
            )


            # ---------------------------------------------------------
            # IMPORTANT:
            # Only remember UI AFTER generation + validation + save
            # + WebSocket sending all succeed.
            # ---------------------------------------------------------

            last_ui_type = ui_type


    except WebSocketDisconnect:

        manager.disconnect(websocket)

        print("Frontend Disconnected")


    except Exception:

        logger.exception(
            "Unexpected WebSocket error"
        )

        manager.disconnect(websocket)

        print("WebSocket disconnected because of error")