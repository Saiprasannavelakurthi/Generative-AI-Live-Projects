from utils.validator import validate_component


def test_empty():
    status, message = validate_component("")

    assert status is False
    assert "Empty response" in message


def test_markdown():
    code = """
```jsx
const Component = () => <div>Hello</div>;
    ```
    """

    status, message = validate_component(code)

    assert status is False
    assert "markdown" in message.lower()


def test_missing_component_name():

    code = """
    const Login = () => {
        return <div>Hello</div>;
    };
    """

    status, message = validate_component(code)

    assert status is False
    assert "Component" in message


def test_missing_arrow_function():

    code = """
    const Component() {
        return <div>Hello</div>;
    }
    """

    status, message = validate_component(code)

    assert status is False


def test_import_not_allowed():

    code = """
    import React from "react";

    const Component = () => {
        return <div>Hello</div>;
    };
    """

    status, message = validate_component(code)

    assert status is False
    assert "Import" in message


def test_export_not_allowed():

    code = """
    const Component = () => {
        return <div>Hello</div>;
    };

    export default Component;
    """

    status, message = validate_component(code)

    assert status is False
    assert "Export" in message


def test_unbalanced_braces():

    code = """
    const Component = () => {
        return (
            <div>Hello</div>
        );
    """

    status, message = validate_component(code)

    assert status is False
    assert "braces" in message.lower() or "babel" in message.lower()


def test_unbalanced_parentheses():

    code = """
    const Component = () => {
        return (
            <div>Hello</div>;
        };
    """

    status, message = validate_component(code)

    assert status is False
    assert "parentheses" in message.lower() or "babel" in message.lower()


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

    status, message = validate_component(code)

    assert status is True
    assert message == "React component is valid."