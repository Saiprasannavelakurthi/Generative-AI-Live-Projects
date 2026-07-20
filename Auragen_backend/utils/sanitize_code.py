import re


def sanitize_component_code(code: str) -> str:
    """
    Normalize LLM-generated JSX before it reaches the browser's Babel
    compiler.

    The prompt tells the model to: name the root component `Component`,
    never wrap output in markdown fences, and never use import/export
    statements. Models don't always follow that reliably, so this
    function defensively cleans up the most common violations instead
    of letting broken code reach the frontend as-is.
    """

    if not code:
        return code

    code = code.strip()

    # --- Strip markdown code fences, e.g. ```jsx ... ``` or ``` ... ```
    code = re.sub(r'^```[a-zA-Z]*\s*\n?', '', code)
    code = re.sub(r'\n?```\s*$', '', code)
    code = code.strip()

    # --- Remove import statements (sandbox has no module system)
    code = re.sub(r'^\s*import .*?;?\s*$', '', code, flags=re.MULTILINE)

    # --- Find "export default X;" (or "export default function X" /
    #     "export default () => ..."), remember the name if there is one,
    #     then strip the "export default" keyword entirely.
    export_match = re.search(
        r'export\s+default\s+([A-Za-z_$][A-Za-z0-9_$]*)\s*;?',
        code
    )
    root_name = export_match.group(1) if export_match else None

    code = re.sub(r'export\s+default\s+([A-Za-z_$][A-Za-z0-9_$]*)\s*;?', '', code)
    code = re.sub(r'export\s+default\s+', '', code)

    code = code.strip()

    already_has_component = bool(
        re.search(r'\bfunction\s+Component\b', code)
        or re.search(r'\bconst\s+Component\s*=', code)
    )

    if not already_has_component and not root_name:
        # No "export default Name" was found — fall back to the first
        # top-level function or const declaration in the file.
        m = re.search(
            r'(?:function\s+([A-Za-z_$][A-Za-z0-9_$]*)\s*\()'
            r'|(?:const\s+([A-Za-z_$][A-Za-z0-9_$]*)\s*=)',
            code
        )
        if m:
            root_name = m.group(1) or m.group(2)

    # --- If the root component isn't literally named "Component",
    #     alias it so the frontend's `typeof Component !== "undefined"`
    #     check succeeds.
    if not already_has_component and root_name and root_name != "Component":
        code += f"\n\nconst Component = {root_name};"

    return code.strip()