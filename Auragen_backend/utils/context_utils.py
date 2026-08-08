from typing import Any

from config import MAX_DOM_LENGTH
from utils.logger import logger


# ==========================================================
# DOM Context
# ==========================================================

import re

def prepare_dom_context(dom_state: str | None) -> str:
    """
    Clean, sanitize, and compress DOM content before sending it to the LLM.
    Prunes noisy inline SVGs, script tags, style attributes, and data URIs.
    """

    if not dom_state:
        return "No DOM state provided."

    # Remove script and style elements
    cleaned = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", dom_state, flags=re.DOTALL | re.IGNORECASE)
    # Remove SVG path data (d="...") which consumes thousands of tokens
    cleaned = re.sub(r'd="[^"]+"', 'd="..."', cleaned)
    # Remove inline base64 image data URIs
    cleaned = re.sub(r'src="data:image/[^"]+"', 'src="..."', cleaned)
    # Collapse multiple whitespaces
    cleaned = " ".join(cleaned.split())

    if len(cleaned) > MAX_DOM_LENGTH:
        cleaned = cleaned[: MAX_DOM_LENGTH - 3] + "..."

    return cleaned


# ==========================================================
# Session Context Store
# ==========================================================

_context_store: dict[str, dict[str, Any]] = {}


def save_context(
    session_id: str,
    page_name: str,
    current_component: str,
    active_field: str,
    form_data: dict,
    cognitive_score: float,
    user_action: str,
) -> None:
    """
    Save the latest UI context for a user session.
    """

    if not session_id:
        return

    _context_store[session_id] = {
        "page_name": page_name,
        "current_component": current_component,
        "active_field": active_field,
        "form_data": form_data.copy(),
        "cognitive_score": cognitive_score,
        "user_action": user_action,
    }

    logger.info(f"Context saved: {session_id}")


def get_context(session_id: str) -> dict[str, Any]:
    """
    Return the stored session context.
    """

    return _context_store.get(session_id, {})


def update_context(
    session_id: str,
    new_values: dict[str, Any],
) -> None:
    """
    Update an existing session context.
    """

    if not session_id:
        return

    if session_id not in _context_store:
        _context_store[session_id] = {}

    _context_store[session_id].update(new_values)

    logger.info(f"Context updated: {session_id}")


def clear_context(session_id: str) -> None:
    """
    Remove a completed session.
    """

    if session_id in _context_store:
        del _context_store[session_id]
        logger.info(f"Context cleared: {session_id}")


def context_exists(session_id: str) -> bool:
    """
    Check whether a session exists.
    """

    return session_id in _context_store


def context_count() -> int:
    """
    Return the number of active sessions.
    """

    return len(_context_store)


def clear_all_context() -> None:
    """
    Clear every stored session.
    """

    _context_store.clear()

    logger.info("All session contexts cleared.")