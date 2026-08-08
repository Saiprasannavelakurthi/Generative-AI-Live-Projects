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
    MINIMAL_PROFILE,
    MINIMAL_UI,
    PROFILE_PAGE,
    REGISTER_FORM,
    RICH_CONTACT,
    RICH_DASHBOARD,
    RICH_LOAN_FORM,
    RICH_LOGIN,
    RICH_PROFILE,
    RICH_REGISTER,
    SIMPLE_UI,
    WIZARD_CONTACT,
    WIZARD_LOAN_FORM,
    WIZARD_LOGIN,
    WIZARD_REGISTER,
)


class PromptBuilder:
    """
    Maps UI types to their corresponding prompt templates.
    """

    def __init__(self):
        self.prompt_map = {
            # Login
            "rich_login": RICH_LOGIN,
            "simple_login": LOGIN_FORM,
            "wizard_login": WIZARD_LOGIN,
            "minimal_login": MINIMAL_LOGIN,

            # Registration
            "rich_register": RICH_REGISTER,
            "registration_form": REGISTER_FORM,
            "wizard_register": WIZARD_REGISTER,

            # Dashboard
            "rich_dashboard": RICH_DASHBOARD,
            "dashboard": DASHBOARD,
            "minimal_dashboard": MINIMAL_DASHBOARD,

            # Loan
            "rich_loan_form": RICH_LOAN_FORM,
            "loan_form": LOAN_FORM,
            "wizard_loan_form": WIZARD_LOAN_FORM,
            "loan_salary_helper": LOAN_SALARY_HELPER,
            "loan_income_helper": LOAN_INCOME_HELPER,
            "minimal_loan_form": MINIMAL_LOAN_FORM,

            # Profile
            "rich_profile": RICH_PROFILE,
            "profile_page": PROFILE_PAGE,
            "minimal_profile": MINIMAL_PROFILE,

            # Contact
            "rich_contact": RICH_CONTACT,
            "contact_form": CONTACT_FORM,
            "wizard_contact": WIZARD_CONTACT,

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