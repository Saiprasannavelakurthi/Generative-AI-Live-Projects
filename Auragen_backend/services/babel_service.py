import json
import subprocess
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
PARSER_PATH = BASE_DIR / "babel_parser" / "parser.js"


def validate_with_babel(code: str):

    try:
        result = subprocess.run(
            ["node", str(PARSER_PATH)],
            input=code,
            text=True,
            capture_output=True,
            timeout=10,
            cwd=str(BASE_DIR / "babel_parser")
        )

        # Node failed
        if result.returncode != 0:
            return {
                "valid": False,
                "message": (
                    result.stderr.strip()
                    or "Babel parser execution failed."
                )
            }

        # Node returned no output
        stdout = result.stdout.strip()

        if not stdout:
            return {
                "valid": False,
                "message": (
                    result.stderr.strip()
                    or "Babel parser returned empty output."
                )
            }

        # Parse Node JSON response
        try:
            return json.loads(stdout)

        except json.JSONDecodeError:
            return {
                "valid": False,
                "message": f"Invalid Babel response: {stdout}"
            }

    except subprocess.TimeoutExpired:
        return {
            "valid": False,
            "message": "Babel validation timed out."
        }

    except FileNotFoundError:
        return {
            "valid": False,
            "message": "Node.js executable was not found."
        }

    except Exception as e:
        return {
            "valid": False,
            "message": f"Babel validation error: {str(e)}"
        }