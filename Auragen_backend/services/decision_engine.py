from utils.logger import logger


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

        page = page_name.strip().lower()
        field = active_field.strip().lower()
        action = user_action.strip().lower()

        score = max(0.0, min(score, 10.0))

        decision = "minimal_ui"

        # ============================
        # Login Page
        # ============================

        if page == "login":

            if score < 3:
                decision = "simple_login"

            elif score < 6:
                decision = "login_dashboard"

            else:
                decision = "minimal_login"

        # ============================
        # Dashboard
        # ============================

        elif page == "dashboard":

            if score < 3:
                decision = "rich_dashboard"

            elif score < 6:
                decision = "dashboard"

            else:
                decision = "minimal_dashboard"

        # ============================
        # Loan Form
        # ============================

        elif page == "loan":

            if field == "salary":
                decision = "loan_salary_helper"

            elif field == "income":
                decision = "loan_income_helper"

            elif score > 6:
                decision = "minimal_loan_form"

            else:
                decision = "loan_form"

        # ============================
        # Registration
        # ============================

        elif page == "register":

            if score > 6:
                decision = "minimal_registration"
            else:
                decision = "registration_form"

        # ============================
        # User Behaviour
        # ============================

        elif action == "scrolling":
            decision = "compact_layout"

        elif action == "typing":
            decision = current_component or "form_layout"

        elif action == "clicking":
            decision = current_component or "interactive_layout"

        # ============================
        # Default
        # ============================

        else:

            if score < 3:
                decision = "simple_ui"

            elif score < 6:
                decision = "dashboard"

            else:
                decision = "minimal_ui"

        logger.info(
            f"DecisionEngine selected '{decision}' "
            f"(page={page}, score={score}, action={action})"
        )

        return decision


decision_engine = DecisionEngine()