from unittest.mock import MagicMock, patch

from services.groq_service import GroqService, _get_fallback_component


def test_fallback_component_generation():
    login_messages = [MagicMock(content="Generate a simple_login UI for login page")]
    code = _get_fallback_component(login_messages)
    assert "const Component" in code
    assert "Welcome Back" in code

    dashboard_messages = [MagicMock(content="Generate dashboard layout")]
    dash_code = _get_fallback_component(dashboard_messages)
    assert "const Component" in dash_code
    assert "Dashboard" in dash_code


def test_groq_service_fallback_on_error():
    service = GroqService()

    # Mock _create_llm to raise error on first model and succeed on second model
    mock_llm1 = MagicMock()
    mock_llm1.invoke.side_effect = Exception("Rate limit 429")

    mock_llm2 = MagicMock()
    mock_response = MagicMock()
    mock_response.content = "const Component = () => <div>Success Fallback</div>;"
    mock_llm2.invoke.return_value = mock_response

    def mock_create(model_name):
        if "instant" in model_name:
            return mock_llm1
        return mock_llm2

    with patch.object(service, "_create_llm", side_effect=mock_create):
        res = service.generate([MagicMock(content="test prompt")])
        assert "Success Fallback" in res
