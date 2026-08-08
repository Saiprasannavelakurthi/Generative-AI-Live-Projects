import json
import os
import subprocess

from utils.logger import logger


def validate_with_babel(code: str) -> dict:
    """
    Validate generated React JSX using the Babel parser.

    Returns:
        {
            "valid": bool,
            "message": str
        }
    """

    base_dir = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )

    parser_path = os.path.join(
        base_dir,
        "babel_parser",
        "parser.js",
    )

    if not os.path.exists(parser_path):
        return {
            "valid": False,
            "message": f"Babel parser not found: {parser_path}",
        }

    try:

        result = subprocess.run(
            ["node", parser_path],
            input=code,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=10,
        )

        if result.returncode != 0:

            logger.error(
                "Babel parser returned an error."
            )

            return {
                "valid": False,
                "message": result.stderr.strip()
                or "Babel parser execution failed.",
            }

        output = result.stdout.strip()

        if not output:

            return {
                "valid": False,
                "message": "Babel parser returned empty output.",
            }

        try:

            parsed = json.loads(output)

            logger.info(
                "Babel validation completed successfully."
            )

            return parsed

        except json.JSONDecodeError:

            logger.error(
                "Invalid JSON returned by Babel parser."
            )

            return {
                "valid": False,
                "message": f"Invalid parser output: {output}",
            }

    except FileNotFoundError:

        logger.error("Node.js is not installed.")

        return {
            "valid": False,
            "message": "Node.js executable not found.",
        }

    except subprocess.TimeoutExpired:

        logger.error("Babel parser timed out.")

        return {
            "valid": False,
            "message": "Babel validation timed out.",
        }

    except Exception as e:

        logger.exception(
            "Unexpected Babel validation error."
        )

        return {
            "valid": False,
            "message": str(e),
        }
