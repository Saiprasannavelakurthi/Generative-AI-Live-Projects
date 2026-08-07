import hashlib
import json
import time
from typing import Any

from config import CACHE_TTL
from utils.logger import logger

# ==========================================================
# In-memory Cache
# ==========================================================

_cache: dict[str, dict[str, Any]] = {}

_cache_hits = 0
_cache_misses = 0


# ==========================================================
# Cache Cleanup
# ==========================================================

def cleanup_expired_cache() -> None:
    """
    Remove expired cache entries.
    """

    current_time = time.time()

    expired_keys = [
        key
        for key, value in _cache.items()
        if current_time - value["created"] > CACHE_TTL
    ]

    for key in expired_keys:
        _cache.pop(key, None)

    if expired_keys:
        logger.info(
            f"Removed {len(expired_keys)} expired cache entries."
        )


# ==========================================================
# Cache Key
# ==========================================================

def create_cache_key(
    prompt: str,
    dom_state: str,
    form_data: dict,
    session_id: str = "",
    page_name: str = "",
    current_component: str = "",
    active_field: str = "",
    cognitive_score: float = 0.0,
    user_action: str = "",
) -> str:
    """
    Create a deterministic cache key.
    """

    payload = {
        "prompt": prompt,
        "dom_state": dom_state,
        "form_data": form_data,
        "session_id": session_id,
        "page_name": page_name,
        "current_component": current_component,
        "active_field": active_field,
        "cognitive_score": cognitive_score,
        "user_action": user_action,
    }

    raw = json.dumps(
        payload,
        sort_keys=True,
        default=str,
    )

    return hashlib.sha256(
        raw.encode("utf-8")
    ).hexdigest()


# ==========================================================
# Get Cache
# ==========================================================

def get_cached(key: str):
    """
    Retrieve a cached response.
    """

    global _cache_hits
    global _cache_misses

    cleanup_expired_cache()

    item = _cache.get(key)

    if item is None:
        _cache_misses += 1
        logger.info("Cache MISS")
        return None

    _cache_hits += 1
    logger.info("Cache HIT")

    return item["value"]


# ==========================================================
# Save Cache
# ==========================================================

def set_cached(key: str, value: dict) -> None:
    """
    Store a response in cache.
    """

    _cache[key] = {
        "created": time.time(),
        "value": value,
    }

    logger.info("Response cached successfully.")


# ==========================================================
# Clear Cache
# ==========================================================

def clear_cache() -> None:
    """
    Remove all cached responses.
    """

    _cache.clear()

    logger.info("Cache cleared.")


# ==========================================================
# Cache Size
# ==========================================================

def cache_size() -> int:
    """
    Return the number of valid cache entries.
    """

    cleanup_expired_cache()

    return len(_cache)


# ==========================================================
# Cache Statistics
# ==========================================================

def cache_stats() -> dict:
    """
    Return cache usage statistics.
    """

    return {
        "entries": cache_size(),
        "hits": _cache_hits,
        "misses": _cache_misses,
    }