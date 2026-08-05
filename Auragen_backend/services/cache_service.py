import hashlib
import json
import time

from config import CACHE_TTL
from utils.logger import logger

_cache: dict = {}

_cache_hits: int = 0
_cache_misses: int = 0


def cleanup_expired_cache():
    """
    Remove expired cache entries.
    """

    current_time = time.time()

    expired = [

        key

        for key, value in _cache.items()

        if current_time - value["created"] > CACHE_TTL

    ]

    for key in expired:
        _cache.pop(key, None)

    if expired:
        logger.info(
            f"Removed {len(expired)} expired cache entries."
        )


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

    payload = {

        "prompt": prompt,
        "dom_state": dom_state,
        "form_data": form_data,
        "session_id": session_id,
        "page_name": page_name,
        "current_component": current_component,
        "active_field": active_field,
        "cognitive_score": cognitive_score,
        "user_action": user_action

    }

    raw = json.dumps(
        payload,
        sort_keys=True,
        default=str
    )

    return hashlib.sha256(
        raw.encode("utf-8")
    ).hexdigest()


def get_cached(key: str):

    global _cache_hits
    global _cache_misses

    cleanup_expired_cache()

    item = _cache.get(key)

    if not item:

        _cache_misses += 1

        logger.info("Cache MISS")

        return None

    _cache_hits += 1

    logger.info("Cache HIT")

    return item["value"]


def set_cached(key: str, value: dict):

    _cache[key] = {

        "created": time.time(),

        "value": value

    }

    logger.info("Response cached successfully.")


def clear_cache():

    _cache.clear()

    logger.info("Cache cleared.")


def cache_size() -> int:

    cleanup_expired_cache()

    return len(_cache)


def cache_stats() -> dict:
    """
    Return cache statistics.
    """

    return {

        "entries": cache_size(),

        "hits": _cache_hits,

        "misses": _cache_misses

    }