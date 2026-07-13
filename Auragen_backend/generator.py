import os
import re

from prompt import prompt_template
from services.groq_service import groq_service

GENERATED_FOLDER = "generated"

os.makedirs(GENERATED_FOLDER, exist_ok=True)


class ReactGenerator:

    @staticmethod
    def generate_component(user_prompt: str):

        messages = prompt_template.format_messages(
            user_prompt=user_prompt
        )

        jsx_code = groq_service.generate(messages)

        # Create filename
        filename = (
            re.sub(r'[^A-Za-z0-9]', '', user_prompt.title())
            .replace("Create", "")
            .replace("Form", "")
            .strip()
        )

        if filename == "":
            filename = "Component"

        filename += ".jsx"

        filepath = os.path.join(
            GENERATED_FOLDER,
            filename
        )

        # Save JSX file
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(jsx_code)

        return {
            "filename": filename,
            "generated_code": jsx_code
        }


generator = ReactGenerator()