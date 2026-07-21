from utils.security_validator import validate_security


def test_eval():

    valid, message = validate_security("eval(alert())")

    assert valid is False

def test_fetch():

    valid, message = validate_security("fetch('/api')")

    assert valid is False