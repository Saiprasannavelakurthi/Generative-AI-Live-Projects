import re
import time
from prompt import prompt_template
from services.groq_service import groq_service
from utils.logger import logger

class ReactGenerator:

    @staticmethod
    def generate_component(user_prompt: str):
        start = time.time()
        messages = prompt_template.format_messages(
            user_prompt=user_prompt
        )

        jsx_code = groq_service.generate(messages)

        end = time.time()

        print(f"Generation Time: {end - start:.2f} seconds")

        print("\n========== GENERATED JSX ==========")
        print(jsx_code)
        print("==================================\n")

        # Create filename
        filename = (
            re.sub(r'[^A-Za-z0-9]', '', user_prompt.title())
            .replace("Create", "")
            .replace("Form", "")
            .strip()
        )

        if filename == "":
            filename = "Component"

        logger.info(
            f"Generated : {filename}"
        )

        return {
            "filename": filename,
            "generated_code": jsx_code
        }


generator = ReactGenerator()