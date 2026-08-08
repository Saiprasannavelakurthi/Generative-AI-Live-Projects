import time

from config import GENERATION_COOLDOWN


class GenerationController:
    """
    Controls how often a UI can be generated.

    Each browser session has its own cooldown.
    """

    def __init__(self, cooldown_seconds: float = GENERATION_COOLDOWN):
        self.cooldown = cooldown_seconds
        self.last_generation = {}

    def can_generate(self, session_id: str = "default") -> bool:
        now = time.time()

        last = self.last_generation.get(session_id, 0)

        if now - last < self.cooldown:
            return False

        self.last_generation[session_id] = now

        return True

    def reset(self, session_id: str = "default"):
        """
        Force a session to generate again immediately.
        """
        self.last_generation.pop(session_id, None)

    def cleanup(self, max_idle_seconds: float = 600):
        """
        Remove inactive sessions.
        """
        now = time.time()

        expired = [
            session
            for session, last in self.last_generation.items()
            if now - last > max_idle_seconds
        ]

        for session in expired:
            self.last_generation.pop(session, None)


generation_controller = GenerationController()