from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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