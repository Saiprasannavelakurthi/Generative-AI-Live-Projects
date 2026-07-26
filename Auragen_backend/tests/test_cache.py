from services.cache_service import (
    create_cache_key,
    get_cached,
    set_cached
)


def test_cache():

    key = create_cache_key(
        "Create login",
        "<form></form>",
        {"email": "abc@test.com"}
    )

    value = {
        "filename": "Login",
        "generated_code": "test"
    }

    set_cached(key, value)

    result = get_cached(key)

    assert result == value


def test_same_input_same_key():

    key1 = create_cache_key(
        "Login",
        "DOM",
        {"name": "A"}
    )

    key2 = create_cache_key(
        "Login",
        "DOM",
        {"name": "A"}
    )

    assert key1 == key2