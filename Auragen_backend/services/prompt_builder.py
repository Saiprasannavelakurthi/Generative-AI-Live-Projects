class PromptBuilder:

    def build_prompt(self, ui_type):

        if ui_type == "simple_login":
            return "Create a simple React login page."

        elif ui_type == "dashboard":
            return "Create a modern React dashboard."

        elif ui_type == "minimal_ui":
            return "Create a minimal distraction-free React interface."

        else:
            return "Create a simple React page."


prompt_builder = PromptBuilder()