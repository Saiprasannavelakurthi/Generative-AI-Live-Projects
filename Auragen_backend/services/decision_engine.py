from utils.logger import logger


class DecisionEngine:
    """
    Determines which UI layout should be generated
    based on user context and cognitive score.
    """

    def decide_ui(
        self,
        score: float,
        page_name: str = "",
        current_component: str = "",
        active_field: str = "",
        user_action: str = "",
    ) -> str:
        """
        Decide which UI template should be generated.
        """

        page = page_name.strip().lower()
        field = active_field.strip().lower()
        action = user_action.strip().lower()

        # Keep score between 0 and 10
        score = max(0.0, min(score, 10.0))

        decision = "simple_ui"

        # ======================================================
        # Login Page
        # ======================================================

        if page == "login":

            if score < 3:
                decision = "simple_login"

            elif score < 6:
                decision = "dashboard"

            else:
                decision = "minimal_login"

        # ======================================================
        # Dashboard
        # ======================================================

        elif page == "dashboard":

            if score < 3:
                decision = "rich_dashboard"

            elif score < 6:
                decision = "dashboard"

            else:
                decision = "minimal_dashboard"

        # ======================================================
        # Loan Page
        # ======================================================

        elif page == "loan":

            if field == "salary":
                decision = "loan_salary_helper"

            elif field == "income":
                decision = "loan_income_helper"

            elif score > 6:
                decision = "minimal_loan_form"

            else:
                decision = "loan_form"

        # ======================================================
        # Registration
        # ======================================================

        elif page == "register":

            if score > 6:
                decision = "minimal_ui"

            else:
                decision = "registration_form"

        # ======================================================
        # Profile
        # ======================================================

        elif page == "profile":
            decision = "profile_page"

        # ======================================================
        # Contact
        # ======================================================

        elif page == "contact":
            decision = "contact_form"

        # ======================================================
        # User Actions
        # ======================================================

        elif action == "scroll":
            decision = "compact_layout"

        elif action == "input":
            decision = "form_layout"

        elif action == "click":
            decision = "interactive_layout"

        # ======================================================
        # Default Decision
        # ======================================================

        else:

            if score < 3:
                decision = "simple_ui"

            elif score < 6:
                decision = "dashboard"

            else:
                decision = "minimal_ui"

        logger.info(
            f"Decision='{decision}' | "
            f"Page='{page}' | "
            f"Score={score:.2f} | "
            f"Action='{action}'"
        )

        return decision


decision_engine = DecisionEngine()