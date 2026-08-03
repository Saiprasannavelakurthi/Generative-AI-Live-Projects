import json

from routes.generate import sse_event


def test_sse_token_event():

    result = sse_event(
        "token",
        {
            "request_id": "test-123",
            "content": "hello"
        }
    )

    assert "event: token\n" in result
    assert "data:" in result
    assert result.endswith("\n\n")


def test_sse_data_is_valid_json():

    result = sse_event(
        "complete",
        {
            "request_id": "test-123",
            "filename": "Login.jsx"
        }
    )

    data_line = next(
        line
        for line in result.splitlines()
        if line.startswith("data: ")
    )

    payload = json.loads(
        data_line.removeprefix("data: ")
    )

    assert payload["request_id"] == "test-123"
    assert payload["filename"] == "Login.jsx"