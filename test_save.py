from save_code import save_component

sample_code = """
function Login() {

    return (

        <div>

            <h1>Login Page</h1>

        </div>

    );

}
"""

path = save_component("Login", sample_code)

print("Component saved at:")
print(path)