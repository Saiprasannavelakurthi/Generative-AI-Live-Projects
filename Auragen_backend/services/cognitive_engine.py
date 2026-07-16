class CognitiveEngine:
    def __init__(self):
        self.threshold = 70

    def calculate_score(self, events):
        """
        Calculate cognitive load score from telemetry events.
        """

        velocity_score = 0
        acceleration_score = 0
        click_score = 0
        hesitation_score = 0

        for event in events:

            if event.get("type") == "move":

                velocity = event.get("velocity", 0)
                acceleration = abs(event.get("acceleration", 0))
                hesitation = event.get("hesitation", False)

                velocity_score += min(velocity / 5, 25)
                acceleration_score += min(acceleration / 20, 25)

                if hesitation:
                    hesitation_score += 15

            elif event.get("type") == "click":
                click_score += 5

        score = (
            velocity_score
            + acceleration_score
            + click_score
            + hesitation_score
        )

        score = min(score, 100)

        return {
            "score": round(score, 2),
            "high_load": score >= self.threshold
        }


cognitive_engine = CognitiveEngine()