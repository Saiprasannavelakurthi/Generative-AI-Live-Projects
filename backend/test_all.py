from validator import validate_component
from save_code import save_component

generated_code = """
function Login() {

    return (

        <div>

            <h1>Login Page</h1>

        </div>

    );

}
"""

status, message = validate_component(generated_code)

print(message)

if status:
    file_path = save_component("Login", generated_code)
    print("Saved Successfully:", file_path)
else:
    print("Component Not Saved")