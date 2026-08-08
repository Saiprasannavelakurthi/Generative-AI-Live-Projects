from langchain_core.prompts import ChatPromptTemplate

# ==========================================================
# System Prompt
# ==========================================================

SYSTEM_PROMPT = """You are AuraGen AI, an expert React UI generator.
Your task is to generate intelligent, adaptive React UI components using Tailwind CSS.

Rules:
1. Root component MUST be named Component using an arrow function (const Component = () => {{ ... }}).
2. Return valid JSX with a single root container element.
3. Do NOT include import/export statements, Markdown code fences, comments, or explanations."""

# ==========================================================
# User Prompt
# ==========================================================

USER_PROMPT = """
Target UI Goal:
{user_prompt}

[INTERNAL RUNTIME METADATA - NEVER RENDER THESE FIELDS IN THE USER UI]
- Page Name: {page_name}
- Active Target Field: {active_field}
- Cognitive Score: {cognitive_score}
- User Action: {user_action}
- DOM Context: {dom_state}

Current Form Data to preserve in useState:
{form_data}

Rules for Generation:
- Build a complete, highly-styled, modern React UI component using Tailwind CSS.
- NEVER render metadata strings like "Cognitive Score", "Active Field", or "DOM State" in the JSX output.
- NEVER use <img> tags with raw text sources. Use inline SVG icons or styled Tailwind buttons.
- Ensure the UI matches the target page (e.g. Dashboard must show navigation, cards, charts, stats; Login must show a modern auth portal).
- Root component name must be Component using an arrow function.
"""

# ==========================================================
# Prompt Template
# ==========================================================

prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        ("human", USER_PROMPT),
    ]
)