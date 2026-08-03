class DecisionEngine:

    def decide_ui(self, score):

        if score < 30:
            return "simple_login"

        elif score < 60:
            return "dashboard"

        else:
            return "minimal_ui"


decision_engine = DecisionEngine()