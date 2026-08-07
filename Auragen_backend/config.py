import os
from dotenv import load_dotenv

# ==========================================================
# Load Environment Variables
# ==========================================================

load_dotenv()

# ==========================================================
# API Keys
# ==========================================================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY not found. Please add it to your .env file."
    )

# ==========================================================
# AI Model Configuration
# ==========================================================

MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "llama-3.3-70b-versatile",
)

TEMPERATURE = float(
    os.getenv("TEMPERATURE", "0.2")
)

MAX_TOKENS = int(
    os.getenv("MAX_TOKENS", "2048")
)

# ==========================================================
# Cache Configuration
# ==========================================================

CACHE_TTL = int(
    os.getenv("CACHE_TTL", "300")
)

# ==========================================================
# DOM Configuration
# ==========================================================

MAX_DOM_LENGTH = int(
    os.getenv("MAX_DOM_LENGTH", "20000")
)

# ==========================================================
# UI Generation
# ==========================================================

GENERATION_COOLDOWN = int(
    os.getenv("GENERATION_COOLDOWN", "5")
)

# ==========================================================
# Logging
# ==========================================================

LOG_LEVEL = os.getenv(
    "LOG_LEVEL",
    "INFO",
)