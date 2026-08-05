from utils.security_validator import validate_security


def test_eval():

    valid, message = validate_security("eval(alert())")

    assert valid is False
    assert "eval(" in message


def test_fetch():

    valid, message = validate_security("fetch('/api')")

    assert valid is False
    assert "fetch(" in message


def test_local_storage():

    valid, message = validate_security(
        "localStorage.setItem('token','123')"
    )

    assert valid is False
    assert "localStorage" in message


def test_process_env():

    valid, message = validate_security(
        "console.log(process.env.API_KEY)"
    )

    assert valid is False
    assert "process.env" in message


def test_import_function():

    valid, message = validate_security(
        "import('react')"
    )

    assert valid is False
    assert "import(" in message


def test_safe_component():

    code = """
    const Component = () => {
        return (
            <div>Hello World</div>
        );
    };
    """

    valid, message = validate_security(code)

    assert valid is True
    assert message == "Safe"