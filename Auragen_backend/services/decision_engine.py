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
        if "loan" in page:
            page = "loan"
        elif "login" in page or "signin" in page or "auth" in page:
            page = "login"
        elif "dash" in page:
            page = "dashboard"
        elif "register" in page or "signup" in page or "sign-up" in page:
            page = "register"
        elif "profile" in page or "account" in page:
            page = "profile"
        elif "contact" in page or "support" in page:
            page = "contact"
        field = active_field.strip().lower()
        action = user_action.strip().lower()

        # Keep score between 0 and 10
        score = max(0.0, min(score, 10.0))

        decision = "simple_ui"

        is_hesitating = (score > 6.0) or (action == "hesitation")

        # ======================================================
        # Login Page
        # ======================================================

        if page == "login":

            if is_hesitating:
                decision = "wizard_login"

            elif score < 3.0:
                decision = "rich_login"

            else:
                decision = "simple_login"

        # ======================================================
        # Dashboard
        # ======================================================

        elif page == "dashboard":

            if is_hesitating:
                decision = "minimal_dashboard"

            elif score < 3.0:
                decision = "rich_dashboard"

            else:
                decision = "dashboard"

        # ======================================================
        # Loan Page
        # ======================================================

        elif page == "loan":

            if field == "salary":
                decision = "loan_salary_helper"

            elif field == "income":
                decision = "loan_income_helper"

            elif is_hesitating:
                decision = "wizard_loan_form"

            elif score < 3.0:
                decision = "rich_loan_form"

            else:
                decision = "loan_form"

        # ======================================================
        # Registration
        # ======================================================

        elif page == "register":

            if is_hesitating:
                decision = "wizard_register"

            elif score < 3.0:
                decision = "rich_register"

            else:
                decision = "registration_form"

        # ======================================================
        # Profile
        # ======================================================

        elif page == "profile":

            if is_hesitating:
                decision = "minimal_profile"

            elif score < 3.0:
                decision = "rich_profile"

            else:
                decision = "profile_page"

        # ======================================================
        # Contact
        # ======================================================

        elif page == "contact":

            if is_hesitating:
                decision = "wizard_contact"

            elif score < 3.0:
                decision = "rich_contact"

            else:
                decision = "contact_form"

        # ======================================================
        # User Actions (no specific page)
        # Match both short and long forms of action names.
        # ======================================================

        elif action in ("scroll", "scrolling"):
            decision = "compact_layout"

        elif action in ("input", "typing"):
            decision = "form_layout"

        elif action in ("click", "clicking"):
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