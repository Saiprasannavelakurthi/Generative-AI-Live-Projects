DANGEROUS = [
    "eval(",
    "new Function",
    "dangerouslySetInnerHTML",
    "document.write",
    "<script",
    "iframe",
    "XMLHttpRequest",
    "fetch(",
    "localStorage",
    "sessionStorage",
    "cookie",
    "process.env",
    "require(",
    "import(",
    "window.location",
    "settimeout(",
    "setinterval(",
    "websocket",
]

def validate_security(code):
    """
        Validate generated React code for dangerous JavaScript patterns.
    """

    lower_code = code.lower()

    for keyword in DANGEROUS:
        if keyword.lower() in lower_code:
            return False, f"Unsafe keyword found: {keyword}"

    return True, "Safe"