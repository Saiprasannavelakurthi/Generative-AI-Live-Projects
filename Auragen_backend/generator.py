import re

from prompt import prompt_template
from services.groq_service import groq_service
from utils.sanitize_code import sanitize_component_code

class ReactGenerator:

    @staticmethod
    def generate_component(user_prompt: str):

        messages = prompt_template.format_messages(
            user_prompt=user_prompt
        )

        raw_code = groq_service.generate(messages)

<<<<<<< Updated upstream
=======
        print("\n========== RAW GENERATED JSX ==========")
        print(raw_code)
        print("========================================\n")

        jsx_code = sanitize_component_code(raw_code)

        print("\n========== SANITIZED JSX ==========")
        print(jsx_code)
        print("====================================\n")

        if "Component" not in jsx_code:
            raise Exception(
                "AI response did not contain a usable 'Component' "
                "after sanitization — the model likely returned an "
                "unexpected format."
            )

>>>>>>> Stashed changes
        # Create filename
        filename = (
            re.sub(r'[^A-Za-z0-9]', '', user_prompt.title())
            .replace("Create", "")
            .replace("Form", "")
            .strip()
        )

        if filename == "":
            filename = "Component"

        return {
            "filename": filename,
            "generated_code": jsx_code
        }


generator = ReactGenerator()