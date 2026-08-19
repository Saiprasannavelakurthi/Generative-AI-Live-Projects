import os
# pyrefly: ignore [missing-import]
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

# Collect all API keys for rotation (add GROQ_API_KEY_2, _3, _4 in .env for extra quota)
_extra_keys = [
    os.getenv("GROQ_API_KEY_2", ""),
    os.getenv("GROQ_API_KEY_3", ""),
    os.getenv("GROQ_API_KEY_4", ""),
]
GROQ_API_KEYS: list[str] = [GROQ_API_KEY] + [k for k in _extra_keys if k.strip()]

# ==========================================================
# AI Model Configuration
# ==========================================================

MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "llama-3.1-8b-instant",
)

# All free Groq models ordered by speed (fastest first).
# The service will try each one and skip any that are rate-limited.
FALLBACK_MODELS = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "openai/gpt-oss-120b",
    "openai/gpt-oss-20b",
]

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
    os.getenv("MAX_DOM_LENGTH", "400")
)

# ==========================================================
# UI Generation
# ==========================================================

GENERATION_COOLDOWN = int(
    os.getenv("GENERATION_COOLDOWN", "3")
)

# ==========================================================
# Logging
# ==========================================================

LOG_LEVEL = os.getenv(
    "LOG_LEVEL",
    "INFO",
)