from utils.validator import validate_component


def test_empty():
    status, _ = validate_component("")
    assert status is False


def test_markdown():
    code = """
    ```jsx
    const Component = () => <div>Hello</div>;
    ```
    """

    status, _ = validate_component(code)

    assert status is False


def test_valid_component():
    code = """
    const Component = () => {
        return (
            <div className="p-4">
                Hello
            </div>
        );
    };
    """

    status, _ = validate_component(code)

    assert status is True