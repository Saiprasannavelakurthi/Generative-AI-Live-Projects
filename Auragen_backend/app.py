from generator import generator
from fastapi import FastAPI
from fastapi import WebSocket, WebSocketDisconnect
from websocket_manager import manager
from fastapi.middleware.cors import CORSMiddleware
from services.cognitive_engine import cognitive_engine
from services.decision_engine import decision_engine
from services.prompt_builder import prompt_builder

from routes.generate import router as generate_router

app = FastAPI(
    title="AuraGen AI Backend",
    version="1.0.0",
    description="AI Backend for generating React components using Groq + LangChain"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # Change this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Routes
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

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    await manager.connect(websocket)

    print("Frontend Connected")

    try:
        while True:

            data = await websocket.receive_json()

            print("Received:", data)

            if data.get("type") == "telemetry_batch":

                result = cognitive_engine.calculate_score(
                    data.get("events", [])
                )

                print("Cognitive Result:", result)
                ui_type = decision_engine.decide_ui(result["score"])

                print("Selected UI:", ui_type)

                prompt = prompt_builder.build_prompt(ui_type)

                print("Prompt:", prompt)

                await manager.send_json(
                    websocket,
                    {
                        "type": "cognitive_score",
                        "score": result["score"],
                        "high_load": result["high_load"]
                    }
                )

                if True:

                    generated = generator.generate_component(prompt)

                    print("Generated:", generated["filename"])
                    print(generated["generated_code"])

                    await manager.send_json(
                        websocket,
                        {
                            "type": "generated_component",
                            "filename": generated["filename"],
                            "code": generated["generated_code"]
                        }
                    )

            else:

                await manager.send_json(
                    websocket,
                    {
                        "status": "received"
                    }
                )

    except WebSocketDisconnect:

        manager.disconnect(websocket)

        print("Disconnected")