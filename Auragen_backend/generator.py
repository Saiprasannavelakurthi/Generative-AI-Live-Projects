import re
import time

from prompt import prompt_template
from services.cache_service import (
    create_cache_key,
    get_cached,
    set_cached,
)
from services.groq_service import groq_service
from utils.logger import logger


class ReactGenerator:

    @staticmethod
    def generate_component(
        user_prompt: str,
        dom_state: str = "",
        form_data: dict | None = None,
        session_id: str = "",
        page_name: str = "",
        current_component: str = "",
        active_field: str = "",
        cognitive_score: float = 0.0,
        user_action: str = ""
    ):

        if not user_prompt.strip():
            raise ValueError("User prompt cannot be empty.")

        start = time.perf_counter()

        form_data = form_data or {}

        cache_key = create_cache_key(
            prompt=user_prompt,
            dom_state=dom_state,
            form_data=form_data,
            session_id=session_id,
            page_name=page_name,
            current_component=current_component,
            active_field=active_field,
            cognitive_score=cognitive_score,
            user_action=user_action,
        )

        cached_result = get_cached(cache_key)

        if cached_result:

            logger.info("Returning cached component.")

            return cached_result

        messages = prompt_template.format_messages(
            user_prompt=user_prompt,
            dom_state=dom_state or "No DOM state provided.",
            form_data=form_data,
            session_id=session_id,
            page_name=page_name,
            current_component=current_component,
            active_field=active_field,
            cognitive_score=cognitive_score,
            user_action=user_action,
        )

        jsx_code = groq_service.generate(messages)

        elapsed = round(
            time.perf_counter() - start,
            2
        )

        filename = (
            re.sub(r"[^A-Za-z0-9]", "", user_prompt.title())
            .replace("Create", "")
            .replace("Form", "")
            .strip()
        )

        if not filename:
            filename = "Component"

        response = {
            "filename": filename,
            "generated_code": jsx_code,
            "page_name": page_name,
            "session_id": session_id,
            "preserved_data": True,
            "context_version": 3,
        }

        set_cached(cache_key, response)

        logger.info(
            f"Generated: {filename} | "
            f"Page={page_name} | "
            f"Time={elapsed}s"
        )

        return response

    @staticmethod
    def stream_component(
        user_prompt: str,
        dom_state: str = "",
        form_data: dict | None = None,
        session_id: str = "",
        page_name: str = "",
        current_component: str = "",
        active_field: str = "",
        cognitive_score: float = 0.0,
        user_action: str = ""
    ):

        if not user_prompt.strip():
            raise ValueError("User prompt cannot be empty.")

        form_data = form_data or {}

        messages = prompt_template.format_messages(
            user_prompt=user_prompt,
            dom_state=dom_state or "No DOM state provided.",
            form_data=form_data,
            session_id=session_id,
            page_name=page_name,
            current_component=current_component,
            active_field=active_field,
            cognitive_score=cognitive_score,
            user_action=user_action,
        )

        yield from groq_service.stream_generate(messages)


generator = ReactGenerator()