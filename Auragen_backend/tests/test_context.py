from utils.context_utils import prepare_dom_context
from config import MAX_DOM_LENGTH


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