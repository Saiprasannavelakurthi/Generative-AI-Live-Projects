from utils.context_utils import prepare_dom_context


def test_empty_dom():

    result = prepare_dom_context(None)

    assert result == "No DOM state provided."


def test_dom_limit():

    dom = "A" * 30000

    result = prepare_dom_context(dom)

    assert len(result) == 20000