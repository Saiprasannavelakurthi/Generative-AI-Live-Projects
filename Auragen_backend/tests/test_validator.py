from utils.validator import validate_component


def test_empty():

    valid, message = validate_component("")

    assert valid is False

def test_markdown():

    code = """```jsx
const Component = () => <div>Hello</div>;
```"""

    valid, message = validate_component(code)

    assert valid is False


def test_valid_component():

    code = """
const Component = () => (
    <div className="p-4">
        Hello
    </div>
);
"""

    valid, message = validate_component(code)

    assert valid is True


def test_export_rejected():

    code = """
const Component = () => (
    <div>Hello</div>
);

export default Component;
"""

    valid, message = validate_component(code)

    assert valid is False