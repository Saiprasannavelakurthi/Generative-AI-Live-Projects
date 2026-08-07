import re
from datetime import datetime
from pathlib import Path

from utils.logger import logger

# ==========================================================
# Output Folder
# ==========================================================

OUTPUT_FOLDER = Path("generated_UI")


def save_component(filename: str, code: str) -> str:
    """
    Save the generated React component inside the
    generated_UI folder.

    Returns:
        str: Generated filename.
    """

    # Create folder if it does not exist
    OUTPUT_FOLDER.mkdir(
        parents=True,
        exist_ok=True,
    )

    # Remove invalid filename characters
    safe_filename = re.sub(
        r"[^A-Za-z0-9_-]",
        "",
        filename,
    )

    if not safe_filename:
        safe_filename = "Component"

    # Timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    unique_filename = (
        f"{safe_filename}_{timestamp}.jsx"
    )

    filepath = OUTPUT_FOLDER / unique_filename

    filepath.write_text(
        code,
        encoding="utf-8",
    )

    logger.info(
        f"Component saved successfully: {filepath}"
    )

    return unique_filename


if __name__ == "__main__":
    print("✅ Save Component Utility Ready")