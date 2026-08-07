COMMON_RULES = """
Return ONLY a React Functional Component.

Rules:

- The root component name MUST be Component.
- The component MUST use an arrow function.
- Return valid JSX.
- Return a single root JSX element.
- Use Tailwind CSS only.
- Do NOT include import statements.
- Do NOT include export statements.
- Do NOT return Markdown.
- Do NOT return comments.
- Do NOT return explanations.
- Preserve existing form values whenever possible.
"""


# ==========================================================
# LOGIN
# ==========================================================

LOGIN_FORM = f"""
{COMMON_RULES}

Generate a modern login page.

Include:
- Email
- Password
- Remember Me checkbox
- Forgot Password
- Login button

Responsive.
"""


MINIMAL_LOGIN = f"""
{COMMON_RULES}

Generate a distraction-free login page.

Include only:
- Email
- Password
- Login button
"""


# ==========================================================
# REGISTER
# ==========================================================

REGISTER_FORM = f"""
{COMMON_RULES}

Generate a responsive registration page.

Include:
- Username
- Email
- Password
- Confirm Password
- Register button
"""


# ==========================================================
# DASHBOARD
# ==========================================================

DASHBOARD = f"""
{COMMON_RULES}

Generate a professional dashboard.

Include:
- Navbar
- Sidebar
- Statistics cards
- Recent activity
- Responsive layout
"""


RICH_DASHBOARD = f"""
{COMMON_RULES}

Generate an advanced analytics dashboard.

Include:
- Navbar
- Sidebar
- KPI cards
- Charts
- Activity table
- Notifications
- User profile
"""


MINIMAL_DASHBOARD = f"""
{COMMON_RULES}

Generate a simplified dashboard.

Include only:
- Navbar
- Summary cards
"""


# ==========================================================
# LOAN
# ==========================================================

LOAN_FORM = f"""
{COMMON_RULES}

Generate a responsive loan application form.

Include:
- Name
- Income
- Salary
- Loan Amount
- Purpose
- Submit button
"""


LOAN_SALARY_HELPER = f"""
{COMMON_RULES}

Generate a loan application form.

Focus on:
- Salary field
- Salary helper text
- Preserve user data
"""


LOAN_INCOME_HELPER = f"""
{COMMON_RULES}

Generate a loan application form.

Focus on:
- Income field
- Income helper text
- Preserve user data
"""


MINIMAL_LOAN_FORM = f"""
{COMMON_RULES}

Generate a minimal loan application form.

Include only essential fields.
"""


# ==========================================================
# PROFILE
# ==========================================================

PROFILE_PAGE = f"""
{COMMON_RULES}

Generate a user profile page.

Include:
- Avatar
- Name
- Email
- Phone
- Edit Profile button
"""


# ==========================================================
# CONTACT
# ==========================================================

CONTACT_FORM = f"""
{COMMON_RULES}

Generate a contact form.

Include:
- Name
- Email
- Subject
- Message
- Submit button
"""


# ==========================================================
# LAYOUTS
# ==========================================================

COMPACT_LAYOUT = f"""
{COMMON_RULES}

Generate a compact layout suitable for fast scrolling users.
"""


FORM_LAYOUT = f"""
{COMMON_RULES}

Generate a responsive form layout while preserving existing values.
"""


INTERACTIVE_LAYOUT = f"""
{COMMON_RULES}

Generate an interactive UI with emphasis on clickable actions.
"""


# ==========================================================
# DEFAULTS
# ==========================================================

MINIMAL_UI = f"""
{COMMON_RULES}

Generate a minimal distraction-free interface.
"""


SIMPLE_UI = f"""
{COMMON_RULES}

Generate a clean responsive interface.
"""