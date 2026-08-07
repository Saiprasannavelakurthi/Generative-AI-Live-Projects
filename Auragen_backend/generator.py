import re
import time

from prompt import prompt_template

from services.cache_service import (
    create_cache_key,
    get_cached,
    set_cached,
)

from services.groq_service import groq_service
from services.decision_engine import decision_engine
from services.prompt_builder import prompt_builder

from utils.logger import logger


class ReactGenerator:

    @staticmethod
    def build_combined_prompt(
        user_prompt: str,
        page_name: str,
        current_component: str,
        active_field: str,
        cognitive_score: float,
        user_action: str,
    ) -> str:
        """
        Build the final system prompt based on the
        current UI context and cognitive score.
        """

        ui_type = decision_engine.decide_ui(
            score=cognitive_score,
            page_name=page_name,
            current_component=current_component,
            active_field=active_field,
            user_action=user_action,
        )

        system_prompt = prompt_builder.build_prompt(ui_type)

        return (
            f"{system_prompt}\n\n"
            f"User Request:\n{user_prompt}"
        )

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
        user_action: str = "",
    ):
        """
        Generate a React component using Groq.
        """

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

        combined_prompt = ReactGenerator.build_combined_prompt(
            user_prompt=user_prompt,
            page_name=page_name,
            current_component=current_component,
            active_field=active_field,
            cognitive_score=cognitive_score,
            user_action=user_action,
        )

        print("\n========== VALUES BEFORE format_messages ==========")
        print("combined_prompt:")
        print(combined_prompt)

        print("\npage_name:")
        print(page_name)

        print("\ncurrent_component:")
        print(current_component)

        print("\nactive_field:")
        print(active_field)

        print("\ndom_state (first 500 chars):")
        print((dom_state or "")[:500])

        print("\nform_data:")
        print(form_data)

        try:
            print("======== INPUT VARIABLES ========")
            print({
                "user_prompt": combined_prompt,
                "dom_state": dom_state,
                "form_data": form_data,
                "session_id": session_id,
                "page_name": page_name,
                "current_component": current_component,
                "active_field": active_field,
                "cognitive_score": cognitive_score,
                "user_action": user_action,
            })
            messages = prompt_template.format_messages(
                user_prompt=combined_prompt,
                dom_state=dom_state or "No DOM state provided.",
                form_data=form_data,
                session_id=session_id,
                page_name=page_name,
                current_component=current_component,
                active_field=active_field,
                cognitive_score=cognitive_score,
                user_action=user_action,
            )
        except Exception as e:
            print("\n========== FORMAT ERROR ==========")
            print(type(e).__name__)
            print(e)
            raise

        jsx_code = groq_service.generate(messages).strip()

        print("\n===== RAW GROQ =====")
        print(jsx_code)
        print("====================")

        # Ensure the generated output follows
        # AuraGen's required component structure.
        if not re.search(r"const\s+Component\s*=", jsx_code):
            jsx_code = f"""const Component = () => {{
    return (
{jsx_code}
    );
}};"""
            print("\n===== AFTER WRAPPER =====")
            print(jsx_code)
            print("=========================")

        elapsed = round(time.perf_counter() - start, 2)

        filename = (
            re.sub(r"[^A-Za-z0-9]", "", user_prompt.title())
            .replace("Create", "")
            .replace("Form", "")
            .strip()
        )[:50]

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
            user_action: str = "",
    ):
        """
        Stream the generated React component token-by-token.
        """

        if not user_prompt.strip():
            raise ValueError("User prompt cannot be empty.")

        form_data = form_data or {}

        combined_prompt = ReactGenerator.build_combined_prompt(
            user_prompt=user_prompt,
            page_name=page_name,
            current_component=current_component,
            active_field=active_field,
            cognitive_score=cognitive_score,
            user_action=user_action,
        )

        print("\n========== VALUES BEFORE format_messages ==========")
        print("combined_prompt:")
        print(combined_prompt)

        print("\npage_name:")
        print(page_name)

        print("\ncurrent_component:")
        print(current_component)

        print("\nactive_field:")
        print(active_field)

        print("\ndom_state (first 500 chars):")
        print((dom_state or "")[:500])

        print("\nform_data:")
        print(form_data)

        try:
            print("======== INPUT VARIABLES ========")
            print({
                "user_prompt": combined_prompt,
                "dom_state": dom_state,
                "form_data": form_data,
                "session_id": session_id,
                "page_name": page_name,
                "current_component": current_component,
                "active_field": active_field,
                "cognitive_score": cognitive_score,
                "user_action": user_action,
            })
            messages = prompt_template.format_messages(
                user_prompt=combined_prompt,
                dom_state=dom_state or "No DOM state provided.",
                form_data=form_data,
                session_id=session_id,
                page_name=page_name,
                current_component=current_component,
                active_field=active_field,
                cognitive_score=cognitive_score,
                user_action=user_action,
            )
        except Exception as e:
            print("\n========== FORMAT ERROR ==========")
            print(type(e).__name__)
            print(e)
            raise

        for token in groq_service.stream_generate(messages):
            yield token


generator = ReactGenerator()