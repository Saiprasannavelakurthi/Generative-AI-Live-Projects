class CognitiveEngine:
    """
    Calculates a cognitive load score from user telemetry events.
    """

    # ==========================================================
    # Configuration
    # ==========================================================

    MAX_SCORE = 100
    NORMALIZATION_FACTOR = 5.0

    VELOCITY_DIVISOR = 4
    ACCELERATION_DIVISOR = 20

    MAX_VELOCITY_SCORE = 25
    MAX_ACCELERATION_SCORE = 25

    CLICK_SCORE = 15.0
    RAGE_CLICK_THRESHOLD = 3
    RAGE_CLICK_BONUS = 25.0
    HESITATION_SCORE = 25.0
    BACKSPACE_SCORE = 10.0

    def __init__(self):
        self.threshold = 6
        self.session_scores = {}

    def calculate_score(self, events: list, session_id: str | None = None) -> dict:
        """
        Calculate the cognitive load score from telemetry events using a smooth rolling average.
        """

        if not events:
            # Idle / stationary: decay score gradually toward calm baseline (1.0)
            prev_score = self.session_scores.get(session_id, 1.5)
            new_score = max(0.5, round(prev_score * 0.88, 2))
            self.session_scores[session_id] = new_score
            return {
                "score": new_score,
                "high_load": new_score >= self.threshold,
            }

        velocity_score = 0.0
        acceleration_score = 0.0
        click_score = 0.0
        hesitation_score = 0.0
        keyboard_score = 0.0

        click_count = 0
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

                click_count += 1
                click_score += self.CLICK_SCORE

            # ==================================================
            # Keyboard / Typing Event
            # ==================================================

            elif event_type in ("keyboard", "typing", "input"):

                backspaces = int(event.get("backspaces", 0))
                pause_hesitation = bool(event.get("hesitation", False))
                pause_ms = float(event.get("pause_ms", 0))

                keyboard_score += backspaces * self.BACKSPACE_SCORE

                if pause_hesitation or pause_ms >= 1500:
                    hesitation_score += self.HESITATION_SCORE

        if click_count >= self.RAGE_CLICK_THRESHOLD:
            click_score += self.RAGE_CLICK_BONUS * click_count

        batch_score = (
            velocity_score
            + acceleration_score
            + click_score
            + hesitation_score
            + keyboard_score
        )

        batch_normalized = round(
            min(batch_score, self.MAX_SCORE) / self.NORMALIZATION_FACTOR,
            2,
        )

        if not session_id:
            return {
                "score": batch_normalized,
                "high_load": batch_normalized >= self.threshold,
            }

        prev_score = self.session_scores.get(session_id, 1.5)
        # Fast responsive moving average so friction elevates score into >6.0 tier instantly
        smoothed_score = round(0.75 * batch_normalized + 0.25 * prev_score, 2)
        smoothed_score = max(0.1, min(smoothed_score, 10.0))

        self.session_scores[session_id] = smoothed_score

        return {
            "score": smoothed_score,
            "high_load": smoothed_score >= self.threshold,
        }


cognitive_engine = CognitiveEngine()