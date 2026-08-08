import re

# ==========================================================
# Dangerous JavaScript Patterns
# Each entry is (regex_pattern, human_readable_label)
# ==========================================================

DANGEROUS_PATTERNS = [
    (r"eval\s*\(",            "eval("),
    (r"new\s+Function",       "new Function"),
    (r"dangerouslySetInnerHTML", "dangerouslySetInnerHTML"),
    (r"document\.write",      "document.write"),
    (r"<script",              "<script"),
    (r"<iframe",              "<iframe"),
    (r"XMLHttpRequest",       "XMLHttpRequest"),
    (r"\bfetch\s*\(",         "fetch("),
    (r"localStorage",         "localStorage"),
    (r"sessionStorage",       "sessionStorage"),
    (r"document\.cookie",     "document.cookie"),
    (r"process\.env",         "process.env"),
    (r"require\s*\(",         "require("),
    (r"import\s*\(",          "import("),
    (r"window\.location",     "window.location"),
    (r"window\.open",         "window.open"),
    (r"setTimeout\s*\(",      "setTimeout("),
    (r"setInterval\s*\(",     "setInterval("),
    (r"WebSocket",            "WebSocket"),
]


def validate_security(code: str) -> tuple[bool, str]:
    """
    Validate generated React code for potentially unsafe
    JavaScript patterns.

    Returns:
        (True, "Safe")               — code is clean
        (False, "Unsafe: <label>")  — dangerous pattern found
    """

    if not code or not code.strip():
        return False, "Generated code is empty."

    for pattern, label in DANGEROUS_PATTERNS:

        if re.search(
            pattern,
            code,
            flags=re.IGNORECASE,
        ):
            return (
                False,
                f"Unsafe pattern detected: {label}",
            )

    return (
        True,
        "Safe",
    )


if __name__ == "__main__":
    print("✅ Security Validator Running...")