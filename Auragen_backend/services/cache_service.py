import hashlib
import json
import time

from config import CACHE_TTL

_cache = {}


def create_cache_key(
    prompt: str,
    dom_state: str,
    form_data: dict,
    session_id: str = "",
    page_name: str = "",
    current_component: str = "",
    active_field: str = "",
    cognitive_score: float = 0.0,
    user_action: str = ""
):
    """
    Create a unique cache key using all Week 3 context.
    """

    payload = {

        "prompt": prompt,

        "dom_state": dom_state,

        "form_data": form_data,

        # Week 3 Context
        "session_id": session_id,

        "page_name": page_name,

        "current_component": current_component,

        "active_field": active_field,

        "cognitive_score": cognitive_score,

        "user_action": user_action
    }

    raw = json.dumps(
        payload,
        sort_keys=True
    )

    return hashlib.sha256(
        raw.encode("utf-8")
    ).hexdigest()


def get_cached(key: str):
    """
    Return cached value if it is still valid.
    """

    item = _cache.get(key)

    if not item:
        return None

    if time.time() - item["created"] > CACHE_TTL:
        _cache.pop(key, None)
        return None

    return item["value"]


def set_cached(key: str, value):
    """
    Store generated UI in cache.
    """

    _cache[key] = {

        "created": time.time(),

        "value": value

    }


def clear_cache():
    """
    Remove every cached item.
    """

    _cache.clear()


def cache_size():
    """
    Return number of cached entries.
    """

    return len(_cache)