# backend/utils/design_rules.py

DESIGN_RULES = """
===============================
AuraGen Design System
===============================

GENERAL RULES

1. Generate only React Functional Components.
2. Use JSX only.
3. Do NOT return Markdown.
4. Do NOT explain anything.
5. Do NOT use inline CSS.
6. Use Tailwind CSS only.
7. Export component as default.
8. Make components responsive.
9. Keep code production ready.

=================================
COLORS
=================================

Primary:
bg-blue-600

Primary Hover:
hover:bg-blue-700

Secondary:
bg-gray-100

Background:
bg-white

Text:
text-gray-800

=================================
BUTTON

className="
w-full
bg-blue-600
hover:bg-blue-700
text-white
py-3
rounded-xl
font-semibold
transition
"

=================================
INPUT

className="
w-full
border
border-gray-300
rounded-lg
p-3
focus:outline-none
focus:ring-2
focus:ring-blue-500
"

=================================
LABEL

className="
block
text-sm
font-medium
mb-2
text-gray-700
"

=================================
CARD

className="
bg-white
shadow-lg
rounded-xl
p-6
"

=================================
PAGE CONTAINER

className="
min-h-screen
flex
justify-center
items-center
bg-gray-100
"

=================================
HEADING

className="
text-3xl
font-bold
mb-6
text-center
"

=================================
PARAGRAPH

className="
text-gray-500
text-center
mb-4
"

=================================
FORM

className="
space-y-4
"

=================================
ICONS

Use Heroicons if icons are needed.

=================================
LAYOUT

Always center forms.

Maximum width:

max-w-md

=================================
OUTPUT

Return ONLY valid React JSX.

Do NOT return

```jsx

or

Explanation

or

Markdown.
"""