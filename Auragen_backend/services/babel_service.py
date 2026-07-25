import subprocess
import json


def validate_with_babel(code: str):

    result = subprocess.run(

        ["node", "babel_parser/parser.js", code],

        capture_output=True,
        text=True

    )

    return json.loads(result.stdout)