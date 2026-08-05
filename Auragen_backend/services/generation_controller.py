import time

class GenerationController:

    def __init__(self):
        self.last_generation = 0

    def can_generate(self):
        now = time.time()

        if now - self.last_generation < 5:
            return False

        self.last_generation = now
        return True

generation_controller = GenerationController()