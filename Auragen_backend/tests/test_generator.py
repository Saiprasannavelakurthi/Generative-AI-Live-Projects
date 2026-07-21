from generator import ReactGenerator


def test_generate():

    response = ReactGenerator.generate_component(
        "Create Login Form"
    )

    assert "generated_code" in response