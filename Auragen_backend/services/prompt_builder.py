from utils.prompt_templates import (
    COMPACT_LAYOUT,
    CONTACT_FORM,
    DASHBOARD,
    FORM_LAYOUT,
    INTERACTIVE_LAYOUT,
    LOAN_FORM,
    LOAN_INCOME_HELPER,
    LOAN_SALARY_HELPER,
    LOGIN_FORM,
    MINIMAL_DASHBOARD,
    MINIMAL_LOAN_FORM,
    MINIMAL_LOGIN,
    MINIMAL_UI,
    PROFILE_PAGE,
    REGISTER_FORM,
    RICH_DASHBOARD,
    SIMPLE_UI,
)


class PromptBuilder:
    """
    Maps UI types to their corresponding prompt templates.
    """

    def __init__(self):
        self.prompt_map = {
            # Login
            "simple_login": LOGIN_FORM,
            "minimal_login": MINIMAL_LOGIN,

            # Registration
            "registration_form": REGISTER_FORM,

            # Dashboard
            "dashboard": DASHBOARD,
            "rich_dashboard": RICH_DASHBOARD,
            "minimal_dashboard": MINIMAL_DASHBOARD,

            # Loan
            "loan_form": LOAN_FORM,
            "loan_salary_helper": LOAN_SALARY_HELPER,
            "loan_income_helper": LOAN_INCOME_HELPER,
            "minimal_loan_form": MINIMAL_LOAN_FORM,

            # Pages
            "profile_page": PROFILE_PAGE,
            "contact_form": CONTACT_FORM,

            # Layouts
            "compact_layout": COMPACT_LAYOUT,
            "form_layout": FORM_LAYOUT,
            "interactive_layout": INTERACTIVE_LAYOUT,

            # Default
            "minimal_ui": MINIMAL_UI,
            "simple_ui": SIMPLE_UI,
        }

    def build_prompt(self, ui_type: str) -> str:
        """
        Return the prompt template for the given UI type.
        Falls back to SIMPLE_UI if the UI type is unknown.
        """
        return self.prompt_map.get(ui_type, SIMPLE_UI)


prompt_builder = PromptBuilder()