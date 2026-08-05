from services.cache_service import (
    create_cache_key,
    get_cached,
    set_cached,
    clear_cache,
    cache_size,
)


def setup_function():
    """
    Clear cache before every test.
    """
    clear_cache()


def test_cache_save_and_get():

    key = create_cache_key(
        "Create login form",
        "<form></form>",
        {"email": "test@example.com"},
    )

    value = {
        "filename": "Login.jsx",
        "generated_code": "test-code",
    }

    set_cached(key, value)

    result = get_cached(key)

    assert result == value


def test_same_input_same_cache_key():

    key1 = create_cache_key(
        "Create login",
        "<form></form>",
        {"name": "John"},
    )

    key2 = create_cache_key(
        "Create login",
        "<form></form>",
        {"name": "John"},
    )

    assert key1 == key2


def test_different_prompt_different_key():

    key1 = create_cache_key(
        "Create login",
        "<form></form>",
        {},
    )

    key2 = create_cache_key(
        "Create dashboard",
        "<form></form>",
        {},
    )

    assert key1 != key2


def test_form_data_changes_cache_key():

    key1 = create_cache_key(
        "Simplify form",
        "<form></form>",
        {"name": "John"},
    )

    key2 = create_cache_key(
        "Simplify form",
        "<form></form>",
        {"name": "David"},
    )

    assert key1 != key2


def test_dom_changes_cache_key():

    key1 = create_cache_key(
        "Simplify form",
        "<form><input /></form>",
        {},
    )

    key2 = create_cache_key(
        "Simplify form",
        "<form><button /></form>",
        {},
    )

    assert key1 != key2


def test_cache_returns_none_for_missing_key():

    result = get_cached("unknown_key")

    assert result is None


def test_cache_size():

    assert cache_size() == 0

    key = create_cache_key(
        "Create Login",
        "",
        {},
    )

    set_cached(
        key,
        {
            "filename": "Login",
            "generated_code": "code",
        },
    )

    assert cache_size() == 1