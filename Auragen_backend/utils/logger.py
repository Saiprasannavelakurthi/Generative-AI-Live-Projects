import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

# ==========================================================
# Log Directory
# ==========================================================

LOG_DIR = Path("logs")
LOG_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

LOG_FILE = LOG_DIR / "app.log"

# ==========================================================
# Logger
# ==========================================================

logger = logging.getLogger("AuraGen")

logger.setLevel(logging.INFO)

if not logger.handlers:

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    # -----------------------------------------
    # File Logger
    # -----------------------------------------

    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=5 * 1024 * 1024,   # 5 MB
        backupCount=5,
        encoding="utf-8",
    )

    file_handler.setFormatter(formatter)

    # -----------------------------------------
    # Console Logger
    # -----------------------------------------

    console_handler = logging.StreamHandler()

    console_handler.setFormatter(formatter)

    # -----------------------------------------
    # Add Handlers
    # -----------------------------------------

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

logger.propagate = False

# ==========================================================
# Startup Log
# ==========================================================

logger.info("AuraGen Logger Initialized")