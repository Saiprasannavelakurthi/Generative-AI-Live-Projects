import hashlib
import json
import time

from config import CACHE_TTL

_cache = {}


def create_cache_key(
    prompt: str,
    dom_state: str,
    form_data: dict
):

    payload = {
        "prompt": prompt,
        "dom_state": dom_state,
        "form_data": form_data
    }

    raw = json.dumps(
        payload,
        sort_keys=True
    )

    return hashlib.sha256(
        raw.encode("utf-8")
    ).hexdigest()


def get_cached(key: str):

    item = _cache.get(key)

    if not item:
        return None

    if time.time() - item["created"] > CACHE_TTL:
        _cache.pop(key, None)
        return None

    return item["value"]


def set_cached(key: str, value):

    _cache[key] = {
        "created": time.time(),
        "value": value
    }