from utils.prompt_templates import *

class PromptBuilder:

    def __init__(self):

        self.prompt_map = {

            "simple_login": LOGIN_FORM,
            "minimal_login": MINIMAL_LOGIN,

            "registration_form": REGISTER_FORM,

            "dashboard": DASHBOARD,
            "rich_dashboard": RICH_DASHBOARD,
            "minimal_dashboard": MINIMAL_DASHBOARD,

            "loan_form": LOAN_FORM,
            "loan_salary_helper": LOAN_SALARY_HELPER,
            "loan_income_helper": LOAN_INCOME_HELPER,
            "minimal_loan_form": MINIMAL_LOAN_FORM,

            "profile_page": PROFILE_PAGE,
            "contact_form": CONTACT_FORM,

            "compact_layout": COMPACT_LAYOUT,
            "form_layout": FORM_LAYOUT,
            "interactive_layout": INTERACTIVE_LAYOUT,

            "minimal_ui": MINIMAL_UI,
            "simple_ui": SIMPLE_UI,
        }

    def build_prompt(self, ui_type: str) -> str:

        return self.prompt_map.get(ui_type, SIMPLE_UI)


prompt_builder = PromptBuilder()