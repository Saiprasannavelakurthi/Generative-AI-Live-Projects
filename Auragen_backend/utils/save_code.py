import os
from datetime import datetime


def save_component(filename, code):
    """
    Save the generated React component
    inside the generated_ui folder.
    """

    folder = "generated"

    # Create folder if it doesn't exist
    os.makedirs(folder, exist_ok=True)

    # Generate timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = filename.replace(" ", "")

    # Create unique filename
    unique_filename = f"{filename}_{timestamp}.jsx"

    filepath = os.path.join(folder, unique_filename)

    with open(filepath, "w", encoding="utf-8") as file:
        file.write(code)

    return unique_filename

print("✅ Saving component")