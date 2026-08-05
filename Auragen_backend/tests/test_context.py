from utils.context_utils import (
    prepare_dom_context,
    save_context,
    get_context,
    update_context,
    clear_context,
    context_exists,
    context_count,
)

from config import MAX_DOM_LENGTH


def setup_function():
    """
    Clear test session before every test.
    """
    clear_context("test_session")


# =====================================================
# DOM Context Tests
# =====================================================

def test_empty_dom():

    result = prepare_dom_context(None)

    assert result == "No DOM state provided."


def test_normal_dom():

    dom = "<form><input /></form>"

    result = prepare_dom_context(dom)

    assert result == dom


def test_dom_length_limit():

    dom = "A" * (MAX_DOM_LENGTH + 1000)

    result = prepare_dom_context(dom)

    assert len(result) == MAX_DOM_LENGTH


# =====================================================
# Session Context Tests
# =====================================================

def test_save_and_get_context():

    save_context(
        session_id="test_session",
        page_name="login",
        current_component="LoginForm",
        active_field="email",
        form_data={"email": "abc@test.com"},
        cognitive_score=5.0,
        user_action="typing",
    )

    context = get_context("test_session")

    assert context["page_name"] == "login"
    assert context["current_component"] == "LoginForm"
    assert context["active_field"] == "email"
    assert context["form_data"]["email"] == "abc@test.com"
    assert context["cognitive_score"] == 5.0
    assert context["user_action"] == "typing"


def test_update_context():

    save_context(
        session_id="test_session",
        page_name="login",
        current_component="LoginForm",
        active_field="email",
        form_data={},
        cognitive_score=2.0,
        user_action="typing",
    )

    update_context(
        "test_session",
        {
            "page_name": "dashboard",
            "cognitive_score": 7.5,
        },
    )

    context = get_context("test_session")

    assert context["page_name"] == "dashboard"
    assert context["cognitive_score"] == 7.5


def test_context_exists():

    save_context(
        session_id="test_session",
        page_name="login",
        current_component="LoginForm",
        active_field="",
        form_data={},
        cognitive_score=1.0,
        user_action="clicking",
    )

    assert context_exists("test_session") is True


def test_clear_context():

    save_context(
        session_id="test_session",
        page_name="login",
        current_component="LoginForm",
        active_field="",
        form_data={},
        cognitive_score=1.0,
        user_action="typing",
    )

    clear_context("test_session")

    assert context_exists("test_session") is False


def test_context_count():

    save_context(
        session_id="session1",
        page_name="login",
        current_component="Login",
        active_field="",
        form_data={},
        cognitive_score=2.0,
        user_action="typing",
    )

    save_context(
        session_id="session2",
        page_name="dashboard",
        current_component="Dashboard",
        active_field="",
        form_data={},
        cognitive_score=3.0,
        user_action="scrolling",
    )

    assert context_count() >= 2

    clear_context("session1")
    clear_context("session2")