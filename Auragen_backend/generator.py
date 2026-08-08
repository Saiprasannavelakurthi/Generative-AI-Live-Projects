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

from utils.validator import clean_code
from utils.context_utils import prepare_dom_context
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

        logger.debug(f"Combined prompt: {combined_prompt[:200]}")
        logger.debug(f"Page: {page_name}, Component: {current_component}, Field: {active_field}")
        logger.debug(f"DOM state (first 200): {(dom_state or '')[:200]}")
        logger.debug(f"Form data: {form_data}")

        comp_snippet = (current_component[:300] + "...") if len(current_component) > 300 else current_component
        dom_snippet = prepare_dom_context(dom_state)
        try:
            messages = prompt_template.format_messages(
                user_prompt=combined_prompt,
                dom_state=dom_snippet,
                form_data=form_data,
                session_id=session_id,
                page_name=page_name,
                current_component=comp_snippet,
                active_field=active_field,
                cognitive_score=cognitive_score,
                user_action=user_action,
            )
        except Exception as e:
            logger.exception(f"Prompt formatting failed: {e}")
            raise

        jsx_code = groq_service.generate(messages).strip()
        jsx_code = clean_code(jsx_code)

        logger.debug(f"Groq response (first 300): {jsx_code[:300]}")

        # Ensure the generated output follows AuraGen's required Component structure.
        if not (
            re.search(r"const\s+Component\s*=", jsx_code)
            or re.search(r"function\s+Component\s*\(", jsx_code)
        ):
            # Check if there is an alternative root function/const defined e.g. const LoginUI = ...
            match = re.search(r"(?:const|function)\s+([A-Z][a-zA-Z0-9_]*)\s*(?:=|\()", jsx_code)
            if match and match.group(1) not in ("React", "Fragment"):
                root_name = match.group(1)
                jsx_code = re.sub(rf"\b{root_name}\b", "Component", jsx_code)
            else:
                jsx_code = f"const Component = () => {{\n    return (\n{jsx_code}\n    );\n}};"

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
        This is a synchronous generator — call from a thread
        using asyncio.to_thread() in async contexts.
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

        logger.debug(f"Stream combined prompt: {combined_prompt[:200]}")
        logger.debug(f"Page: {page_name}, Component: {current_component}, Field: {active_field}")
        logger.debug(f"DOM state (first 200): {(dom_state or '')[:200]}")
        logger.debug(f"Form data: {form_data}")

        comp_snippet = (current_component[:300] + "...") if len(current_component) > 300 else current_component
        dom_snippet = prepare_dom_context(dom_state)
        try:
            messages = prompt_template.format_messages(
                user_prompt=combined_prompt,
                dom_state=dom_snippet,
                form_data=form_data,
                session_id=session_id,
                page_name=page_name,
                current_component=comp_snippet,
                active_field=active_field,
                cognitive_score=cognitive_score,
                user_action=user_action,
            )
        except Exception as e:
            logger.exception(f"Stream prompt formatting failed: {e}")
            raise

        for token in groq_service.stream_generate(messages):
            yield token


generator = ReactGenerator()