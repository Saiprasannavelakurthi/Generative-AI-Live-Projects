DESIGN_RULES = """
AuraGen Design System

GENERAL RULES

1. Generate ONLY React Functional Components.
2. The root component MUST be named Component.
3. Use an arrow function.
4. Return ONLY React component code.
5. Do NOT return Markdown.
6. Do NOT return explanations.
7. Do NOT return comments.
8. Do NOT return code fences.
9. Do NOT include import statements.
10. Do NOT include export statements.
11. Use JSX only.
12. Use Tailwind CSS only.
13. Never use inline styles.
14. Never use CSS files.
15. Never use external libraries.
16. Never use images from the internet.
17. Never use placeholder APIs.
18. Never use dummy imports.
19. Code must compile successfully.

Component Requirements

- The component must be named Component.
- Use an arrow function.
- Return valid JSX.
- Return a single root element.
- Do not use React fragments.
- Do not include import or export statements.

========================================
LAYOUT

Use responsive Tailwind CSS.

Container:
- For Forms (Login/Sign Up): w-full max-w-md mx-auto p-6
- For Portals & Dashboards (Dashboard/Loan/Profile/Registration): w-full max-w-5xl mx-auto p-6

Card:
- w-full bg-white border border-slate-200 shadow-xl rounded-2xl p-6 transition-all
- Never render oversized text icons (e.g., do NOT create 128px circle icons with letter 'i'). Keep icons small, elegant, and inside headers (w-6 h-6 or w-8 h-8).

========================================
HEADINGS

Use:

- text-3xl
- font-bold
- text-center
- mb-6
- text-gray-800

========================================
LABEL

Use:

- block
- text-sm
- font-medium
- mb-2
- text-gray-700

========================================
INPUT

Use:

- w-full
- border
- border-gray-300
- rounded-lg
- p-3
- focus:outline-none
- focus:ring-2
- focus:ring-blue-500

========================================
BUTTON

Use:

- w-full
- bg-blue-600
- hover:bg-blue-700
- text-white
- font-semibold
- py-3
- rounded-xl
- transition

========================================
FORM

Use:

- space-y-4

========================================
TEXT

Use:

- text-gray-500
- text-center

========================================
ACCESSIBILITY

Every input must include:

- htmlFor
- id
- label

Buttons must contain visible text.

========================================
FORBIDDEN

Never generate:

- import statements
- export statements
- ReactDOM
- createRoot()
- render()
- axios
- fetch()
- XMLHttpRequest
- document.write()
- dangerouslySetInnerHTML
- eval()
- new Function()
- window.location
- localStorage
- sessionStorage
- cookies
- iframe

========================================
OUTPUT

Return ONLY valid React component code.

Do NOT return:

- Markdown
- Explanations
- Comments
- Code fences
"""