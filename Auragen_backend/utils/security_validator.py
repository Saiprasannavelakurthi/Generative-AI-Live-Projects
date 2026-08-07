import re

# ==========================================================
# Dangerous JavaScript Patterns
# ==========================================================

DANGEROUS_PATTERNS = [
    r"eval\s*\(",
    r"new\s+Function",
    r"dangerouslySetInnerHTML",
    r"document\.write",
    r"<script",
    r"<iframe",
    r"XMLHttpRequest",
    r"\bfetch\s*\(",
    r"localStorage",
    r"sessionStorage",
    r"document\.cookie",
    r"process\.env",
    r"require\s*\(",
    r"import\s*\(",
    r"window\.location",
    r"window\.open",
    r"setTimeout\s*\(",
    r"setInterval\s*\(",
    r"WebSocket",
]


def validate_security(code: str) -> tuple[bool, str]:
    """
    Validate generated React code for potentially unsafe
    JavaScript patterns.
    """

    if not code or not code.strip():
        return False, "Generated code is empty."

    for pattern in DANGEROUS_PATTERNS:

        if re.search(
            pattern,
            code,
            flags=re.IGNORECASE,
        ):
            return (
                False,
                f"Unsafe pattern detected: {pattern}",
            )

    return (
        True,
        "Security validation passed.",
    )


if __name__ == "__main__":
    print("✅ Security Validator Running...")