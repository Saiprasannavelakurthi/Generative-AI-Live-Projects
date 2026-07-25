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
]

def validate_security(code):
    """
        Validate generated React code for dangerous JavaScript patterns.
    """

    for keyword in DANGEROUS:
        if keyword in code:
            return False, f"Unsafe keyword found: {keyword}"

    return True, "Safe"