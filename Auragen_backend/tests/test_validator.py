from utils.validator import validate_component


def test_empty():

    valid, message = validate_component("")

    assert valid is False

def test_markdown():

    code = """```jsx
const A=()=>{}
```"""

    valid, message = validate_component(code)

    assert valid is False

def test_no_export():

    code = """
const Login=()=>{

return <div>Hello</div>

}
"""

    valid, message = validate_component(code)

    assert valid is False