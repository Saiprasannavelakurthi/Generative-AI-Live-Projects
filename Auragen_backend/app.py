from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import traceback

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
    allow_origins=["*"],
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

            if data.get("type") != "telemetry_batch":

                await manager.send_json(
                    websocket,
                    {
                        "status": "received"
                    }
                )

                continue

            result = cognitive_engine.calculate_score(
                data.get("events", [])
            )

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
                    "hesitation",
                ]
            )

            print("Should Generate:", should_generate)

            if not should_generate:
                print("Generation skipped.")
                continue

            allowed = generation_controller.can_generate()

            print("Generation Controller:", allowed)

            if not allowed:
                print("Cooldown active.")
                continue

            full_code = ""

            try:

                print("\n========== START GENERATION ==========")

                for token in generator.stream_component(
                    user_prompt=f"Generate a {data.get('page_name', 'login')} page using React Functional Component with Tailwind CSS.",
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

                print("\n========== GENERATED CODE ==========")
                print(full_code)
                print("====================================")

                status, message = validate_component(full_code)

                print("Validation:", status)
                print(message)

                if not status:

                    await manager.send_json(
                        websocket,
                        {
                            "type": "error",
                            "message": message,
                        },
                    )

                    continue

                safe, security_message = validate_security(full_code)

                print("Security:", safe)
                print(security_message)

                if not safe:

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
                    full_code,
                )

                print("Saved:", saved_filename)

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

                print("\n========== COMPLETE SENT ==========")

            except Exception as e:

                print("\n========== EXCEPTION ==========")
                traceback.print_exc()
                print(e)
                print("================================")

                await manager.send_json(
                    websocket,
                    {
                        "type": "error",
                        "message": str(e),
                    },
                )

    except WebSocketDisconnect:

        manager.disconnect(websocket)

        print("Frontend disconnected.")