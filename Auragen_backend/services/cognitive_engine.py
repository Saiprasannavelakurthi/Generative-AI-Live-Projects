class CognitiveEngine:
    """
    Calculates a cognitive load score from user telemetry events.
    """

    # ==========================================================
    # Configuration
    # ==========================================================

    MAX_SCORE = 100
    NORMALIZATION_FACTOR = 10

    VELOCITY_DIVISOR = 5
    ACCELERATION_DIVISOR = 20

    MAX_VELOCITY_SCORE = 25
    MAX_ACCELERATION_SCORE = 25

    CLICK_SCORE = 5
    HESITATION_SCORE = 15

    def __init__(self):
        self.threshold = 6

    def calculate_score(self, events: list) -> dict:
        """
        Calculate the cognitive load score from telemetry events.
        """

        velocity_score = 0.0
        acceleration_score = 0.0
        click_score = 0.0
        hesitation_score = 0.0

        for event in events:

            event_type = event.get("type", "").lower()

            # ==================================================
            # Mouse Movement
            # ==================================================

            if event_type == "move":

                velocity = max(0.0, float(event.get("velocity", 0)))
                acceleration = abs(float(event.get("acceleration", 0)))
                hesitation = bool(event.get("hesitation", False))

                velocity_score += min(
                    velocity / self.VELOCITY_DIVISOR,
                    self.MAX_VELOCITY_SCORE,
                )

                acceleration_score += min(
                    acceleration / self.ACCELERATION_DIVISOR,
                    self.MAX_ACCELERATION_SCORE,
                )

                if hesitation:
                    hesitation_score += self.HESITATION_SCORE

            # ==================================================
            # Click Event
            # ==================================================

            elif event_type == "click":

                click_score += self.CLICK_SCORE

        total_score = (
            velocity_score
            + acceleration_score
            + click_score
            + hesitation_score
        )

        total_score = min(total_score, self.MAX_SCORE)

        normalized_score = round(
            total_score / self.NORMALIZATION_FACTOR,
            2,
        )

        return {
            "score": normalized_score,
            "high_load": normalized_score >= self.threshold,
        }


cognitive_engine = CognitiveEngine()