from unittest.mock import patch
import pytest
from generator import ReactGenerator


@patch("generator.groq_service.generate")
def test_generate_component(mock_generate):

    mock_generate.return_value = """
const Component = () => {
    return (
        <div>
            Login
        </div>
    );
};
"""

    response = ReactGenerator.generate_component(
        user_prompt="Create Login Form"
    )

    assert isinstance(response, dict)

    assert "filename" in response
    assert "generated_code" in response
    assert "page_name" in response
    assert "session_id" in response
    assert "preserved_data" in response
    assert "context_version" in response

    assert response["filename"] == "Login"
    assert response["preserved_data"] is True
    assert response["context_version"] == 3

    mock_generate.assert_called_once()

def test_empty_prompt():

    with pytest.raises(ValueError):

        ReactGenerator.generate_component(
            user_prompt=""
        )