DANGEROUS = [
    "eval(",
    "new Function(",
    "dangerouslySetInnerHTML",
    "document.write(",
    "window.location",
]

def validate_security(code):

    for item in DANGEROUS:

        if item in code:
            return False, f"Unsafe code detected: {item}"

    return True, "Safe"