import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Read API Key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env file")

# Read model name
MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "llama-3.3-70b-versatile"
)

# Initialize Groq Client
client = Groq(
    api_key=GROQ_API_KEY
)

CACHE_TTL = int(
    os.getenv("CACHE_TTL", "300")
)

MAX_DOM_LENGTH = int(
    os.getenv("MAX_DOM_LENGTH", "20000")
)