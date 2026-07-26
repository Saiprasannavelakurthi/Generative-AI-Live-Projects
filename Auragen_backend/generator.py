import re
import time
from prompt import prompt_template
from services.groq_service import groq_service
from utils.logger import logger

class ReactGenerator:

    @staticmethod
    def generate_component(
            user_prompt: str,
            dom_state: str = "",
            form_data: dict | None = None
    ):

        start = time.time()

        form_data = form_data or {}

        messages = prompt_template.format_messages(
            user_prompt=user_prompt,
            dom_state=dom_state or "No DOM state provided.",
            form_data=form_data
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
            f"Generated: {filename} | "
            f"Generation Time: {end - start:.2f}s"
        )

        return {
            "filename": filename,
            "generated_code": jsx_code
        }

    @staticmethod
    def stream_component(
            user_prompt: str,
            dom_state: str = "",
            form_data: dict | None = None
    ):
        form_data = form_data or {}

        messages = prompt_template.format_messages(
            user_prompt=user_prompt,
            dom_state=dom_state or "No DOM state provided.",
            form_data=form_data
        )

        yield from groq_service.stream_generate(
            messages
        )

generator = ReactGenerator()