class DecisionEngine:

    def decide_ui(self, score):

        if score < 3:
            return "simple_login"

        elif score < 6:
            return "dashboard"

        else:
            return "minimal_ui"


decision_engine = DecisionEngine()