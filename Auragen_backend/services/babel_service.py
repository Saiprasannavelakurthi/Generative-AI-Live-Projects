import subprocess
import json
import os


def validate_with_babel(code: str):

    base_dir = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )

    parser_path = os.path.join(
        base_dir,
        "babel_parser",
        "parser.js"
    )

    try:
        result = subprocess.run(
            ["node", parser_path],
            input=code,
            capture_output=True,
            text=True,
            timeout=10
        )

        # Node/Babel crashed
        if result.returncode != 0:
            return {
                "valid": False,
                "message": (
                    result.stderr.strip()
                    or "Babel parser failed."
                )
            }

        output = result.stdout.strip()

        # Nothing returned
        if not output:
            return {
                "valid": False,
                "message": "Babel parser returned no output."
            }

        try:
            return json.loads(output)

        except json.JSONDecodeError:
            return {
                "valid": False,
                "message": f"Invalid Babel parser output: {output}"
            }

    except FileNotFoundError:
        return {
            "valid": False,
            "message": "Node.js was not found."
        }

    except subprocess.TimeoutExpired:
        return {
            "valid": False,
            "message": "Babel validation timed out."
        }

    except Exception as e:
        return {
            "valid": False,
            "message": f"Babel validation error: {str(e)}"
        }