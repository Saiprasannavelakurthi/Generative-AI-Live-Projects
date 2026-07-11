from validator import validate_component

sample_code = """
function Login() {

    return (

        <div>

            <h1>Login</h1>

            <input type="email" />

            <input type="password" />

            <button>Login</button>

        </div>

    );

}
"""

status, message = validate_component(sample_code)

print("Status :", status)
print("Message:", message)