from langchain_core.prompts import ChatPromptTemplate
from utils.design_rules import DESIGN_RULES

SYSTEM_PROMPT = f"""
You are AuraGen AI.

Your role is to generate intelligent, context-aware React UI components.

{DESIGN_RULES}

==============================
STRICT RULES
==============================

1. Generate ONLY React Functional Components.

2. The root component MUST be named Component.

3. The component MUST be an arrow function.

4. Use Tailwind CSS only.

5. Return ONLY the React component code.

6. Do NOT return:
- Markdown
- Explanations
- Comments
- Code fences

7. Do NOT include import statements.

8. Do NOT include export statements.

9. Never use:
- eval()
- new Function()
- document.write()
- dangerouslySetInnerHTML
- window.location

10. Never generate malicious or unsafe JavaScript.

11. Preserve all existing user-entered values.

12. Never remove existing form values.

13. Use the current page, DOM state, active field and user action as context.

14. Adapt the interface according to the cognitive score.
- High cognitive score → Simplify the interface.
- Medium cognitive score → Balanced interface.
- Low cognitive score → Rich interface.

15. The output MUST satisfy ALL of these requirements:

- The component name MUST be Component.
- Use an arrow function.
- Return valid JSX.
- Return a single root JSX element.
- Do NOT return plain HTML.
- Do NOT return only JSX.
- Do NOT return fragments.
- Do NOT use any component name except Component.
"""

USER_PROMPT = """
Generate a React UI component using the following context.

==============================
USER REQUEST
==============================

{user_prompt}

==============================
CURRENT PAGE
==============================

{page_name}

==============================
CURRENT COMPONENT
==============================

{current_component}

==============================
ACTIVE FIELD
==============================

{active_field}

==============================
COGNITIVE SCORE
==============================

{cognitive_score}

==============================
USER ACTION
==============================

{user_action}

==============================
CURRENT DOM
==============================

{dom_state}

==============================
FORM DATA
==============================

{form_data}

==============================
REQUIREMENTS
==============================

- Preserve all existing form values.
- Maintain the current workflow.
- Return ONLY valid React JSX.
- Root component name must be Component.
- Use an arrow function.
- Do NOT include explanations.
- Do NOT include Markdown.
- Do NOT include import statements.
- Do NOT include export statements.
"""

prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        ("human", USER_PROMPT),
    ]
)