class DecisionEngine:

    def decide_ui(
        self,
        score: float,
        page_name: str = "",
        current_component: str = "",
        active_field: str = "",
        user_action: str = ""
    ):
        """
        Decide which UI should be generated based on
        the user's cognitive load and current context.
        """

        # ============================
        # Login Page
        # ============================

        if page_name.lower() == "login":

            if score < 3:
                return "simple_login"

            elif score < 6:
                return "login_dashboard"

            else:
                return "minimal_login"

        # ============================
        # Dashboard
        # ============================

        elif page_name.lower() == "dashboard":

            if score < 3:
                return "rich_dashboard"

            elif score < 6:
                return "dashboard"

            else:
                return "minimal_dashboard"

        # ============================
        # Loan Form
        # ============================

        elif page_name.lower() == "loan":

            if active_field.lower() == "salary":
                return "loan_salary_helper"

            elif active_field.lower() == "income":
                return "loan_income_helper"

            elif score > 6:
                return "minimal_loan_form"

            else:
                return "loan_form"

        # ============================
        # Registration
        # ============================

        elif page_name.lower() == "register":

            if score > 6:
                return "minimal_registration"

            return "registration_form"

        # ============================
        # User Behaviour
        # ============================

        if user_action.lower() == "scrolling":
            return "compact_layout"

        if user_action.lower() == "typing":
            return current_component or "form_layout"

        if user_action.lower() == "clicking":
            return current_component or "interactive_layout"

        # ============================
        # Default
        # ============================

        if score < 3:
            return "simple_ui"

        elif score < 6:
            return "dashboard"

        return "minimal_ui"


decision_engine = DecisionEngine()