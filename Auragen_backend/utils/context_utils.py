from config import MAX_DOM_LENGTH


def prepare_dom_context(dom_state: str | None) -> str:
    """
    Clean and limit DOM content before sending to the LLM.
    """

    if not dom_state:
        return "No DOM state provided."

    dom_state = dom_state.strip()

    if len(dom_state) > MAX_DOM_LENGTH:
        dom_state = dom_state[:MAX_DOM_LENGTH]

    return dom_state


# ====================================================
# Week 3 Context Functions
# ====================================================

_context_store = {}


def save_context(
    session_id: str,
    page_name: str,
    current_component: str,
    active_field: str,
    form_data: dict,
    cognitive_score: float,
    user_action: str
):
    """
    Save the latest UI context for a user session.
    """

    _context_store[session_id] = {

        "page_name": page_name,

        "current_component": current_component,

        "active_field": active_field,

        "form_data": form_data,

        "cognitive_score": cognitive_score,

        "user_action": user_action

    }


def get_context(session_id: str) -> dict:
    """
    Return stored context for a session.
    """

    return _context_store.get(session_id, {})


def update_context(
    session_id: str,
    new_values: dict
):
    """
    Update an existing session context.
    """

    if session_id not in _context_store:
        _context_store[session_id] = {}

    _context_store[session_id].update(new_values)


def clear_context(session_id: str):
    """
    Remove a completed session.
    """

    if session_id in _context_store:
        del _context_store[session_id]