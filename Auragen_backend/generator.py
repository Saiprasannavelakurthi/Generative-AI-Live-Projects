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
            form_data: dict | None = None,

            # ===== Week 3 =====
            session_id: str = "",
            page_name: str = "",
            current_component: str = "",
            active_field: str = "",
            cognitive_score: float = 0.0,
            user_action: str = ""
    ):

        start = time.time()

        form_data = form_data or {}

        messages = prompt_template.format_messages(

            user_prompt=user_prompt,

            dom_state=dom_state or "No DOM state provided.",

            form_data=form_data,

            # ===== Week 3 =====

            session_id=session_id,

            page_name=page_name,

            current_component=current_component,

            active_field=active_field,

            cognitive_score=cognitive_score,

            user_action=user_action

        )

        jsx_code = groq_service.generate(messages)

        end = time.time()

        print(f"Generation Time: {end-start:.2f} seconds")

        print("\n========== GENERATED JSX ==========")
        print(jsx_code)
        print("==================================\n")

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
            f"Page={page_name} | "
            f"Score={cognitive_score} | "
            f"Generation Time={end-start:.2f}s"
        )

        return {
            "filename": filename,
            "generated_code": jsx_code,
            "page_name": page_name,
            "session_id": session_id,
            "preserved_data": True,
            "context_version": 3
        }

    @staticmethod
    def stream_component(
            user_prompt: str,
            dom_state: str = "",
            form_data: dict | None = None,

            # ===== Week 3 =====

            session_id: str = "",
            page_name: str = "",
            current_component: str = "",
            active_field: str = "",
            cognitive_score: float = 0.0,
            user_action: str = ""
    ):

        form_data = form_data or {}

        messages = prompt_template.format_messages(

            user_prompt=user_prompt,

            dom_state=dom_state or "No DOM state provided.",

            form_data=form_data,

            # ===== Week 3 =====

            session_id=session_id,

            page_name=page_name,

            current_component=current_component,

            active_field=active_field,

            cognitive_score=cognitive_score,

            user_action=user_action

        )

        yield from groq_service.stream_generate(
            messages
        )


generator = ReactGenerator()