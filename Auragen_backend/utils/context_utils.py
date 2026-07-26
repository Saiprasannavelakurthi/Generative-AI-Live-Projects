MAX_DOM_LENGTH = 20_000


def prepare_dom_context(dom_state: str | None) -> str:

    if not dom_state:
        return "No DOM state provided."

    dom_state = dom_state.strip()

    if len(dom_state) > MAX_DOM_LENGTH:
        dom_state = dom_state[:MAX_DOM_LENGTH]

    return dom_state