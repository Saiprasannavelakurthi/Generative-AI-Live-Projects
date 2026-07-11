import os

def save_component(filename, code):
    """
    Save the generated React component
    inside the generated_ui folder.
    """

    folder = "generated_ui"

    # Create folder if it doesn't exist
    os.makedirs(folder, exist_ok=True)

    filepath = os.path.join(folder, f"{filename}.jsx")

    with open(filepath, "w", encoding="utf-8") as file:
        file.write(code)

    return filepath