class CognitiveEngine:

    def __init__(self):
        # Cognitive load range: 0 - 100
        self.threshold = 60

    def calculate_score(self, events):

        velocity_score = 0
        acceleration_score = 0
        click_score = 0
        hesitation_score = 0

        for event in events:

            event_type = event.get("type")

            # Mouse movement
            if event_type == "move":

                velocity = event.get("velocity", 0)
                acceleration = abs(
                    event.get("acceleration", 0)
                )

                velocity_score += min(
                    velocity * 1.5,
                    30
                )

                acceleration_score += min(
                    acceleration * 2,
                    30
                )

            # User clicks
            elif event_type == "click":

                click_score += 10

            # User hesitation
            elif event_type == "hesitation":

                hesitation_score += 20

        score = (
            velocity_score
            + acceleration_score
            + click_score
            + hesitation_score
        )

        # Keep score between 0 and 100
        score = max(0, min(score, 100))

        return {
            "score": round(score, 2),
            "high_load": score >= self.threshold
        }


cognitive_engine = CognitiveEngine()