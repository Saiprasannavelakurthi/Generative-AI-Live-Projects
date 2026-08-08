COMMON_RULES = """
Return ONLY a React Functional Component. No imports, no exports, no Markdown fences, no comments.

Rules:
- Root component MUST be named Component as an arrow function.
- Return valid JSX with a single root element.
- Use Tailwind CSS for all styling (rounded-2xl, shadow-xl, gradient backgrounds, indigo/blue palette).
- Login/Register: max-w-md mx-auto. Dashboard/Loan/Profile/Contact: max-w-5xl mx-auto grid layout.
- Build real interactive elements. Never output unstyled text.
- No giant circle icons. No long SVG path strings (d="..."). Use text badges instead.
- No <img> tags with raw text.
- Always camelCase variables. Never "Form Data".
- Always define all event handlers (e.g. const handleChange = (e) => {...}).
- Complete all ternary operators: condition ? trueVal : falseVal.
"""


# ==========================================================
# LOGIN
# ==========================================================

RICH_LOGIN = f"""
{COMMON_RULES}

Generate a feature-rich, modern login card for calm users using Tailwind CSS styling.

Include:
- Centered Card Container (max-w-md bg-white border border-slate-200 rounded-2xl shadow-xl p-8).
- Header: Logo icon, Title "Welcome Back", Subtitle "Sign in to access your dashboard".
- Styled Email & Password Input fields with focus outline rings.
- Social SSO Sign-In Row: Styled buttons for "Google", "GitHub", "Enterprise SSO" (Use inline SVG icons or styled text buttons. Do NOT use <img> tags).
- Remember Me checkbox & Forgot Password link.
- Large Primary Sign In button (w-full bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-3 rounded-xl transition shadow-md).
"""


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


WIZARD_LOGIN = f"""
{COMMON_RULES}

Generate a distraction-free conversational step-by-step login wizard for struggling users.

Include:
- Step 1 of 2 indicator bar
- Large email input field with prominent helper tooltip
- Large "Continue →" action button
- Clean minimal layout with high contrast and zero clutter
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

RICH_REGISTER = f"""
{COMMON_RULES}

Generate an advanced registration portal for calm users.

Include:
- Account Type selector (Personal vs Business)
- Full Name, Email, Password fields
- Password strength indicator bar
- Terms & Privacy policy checkbox
- Benefits showcase side panel
- Register button
"""


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


WIZARD_REGISTER = f"""
{COMMON_RULES}

Generate a conversational 2-step signup wizard for struggling users.

Include:
- Step progress bar (Step 1: Account Info, Step 2: Password)
- Extra-large input fields with helpful inline tooltips
- Prominent "Next Step →" button
- Clean single-column distraction-free layout
"""


# ==========================================================
# DASHBOARD
# ==========================================================

DASHBOARD = f"""
{COMMON_RULES}

Generate a clean professional dashboard page with full Tailwind CSS layout.

Include:
- Top Navigation Header with Logo, Navigation Links, and User Avatar.
- Row of 3 Metric Cards (Total Revenue $124,500, Active Users 1,420, Growth +18%).
- Recent Transactions Table with status badges (Completed, Pending, Approved).
"""


RICH_DASHBOARD = f"""
{COMMON_RULES}

Generate an advanced analytics dashboard with full Tailwind CSS grid layout.

Include:
- Top Header: Logo "AuraGen Analytics", Search bar, User Avatar badge, and Notification bell button.
- Main Grid Layout (Sidebar + Dashboard Content):
  - Left Sidebar: Navigation items (Dashboard, Analytics, Loans, Profile, Settings) with active tab highlight.
  - Main Panel:
    - 4 Styled KPI Cards (Revenue $128,400, Active Users 2,840, Monthly Growth +24%, Pending Reviews 8) with trend badges.
    - Performance Overview card with SVG progress/bar indicators.
    - Activity Table with User, Action, Amount, Status Badge, and Date columns.
"""


MINIMAL_DASHBOARD = f"""
{COMMON_RULES}

Generate a clean, simplified distraction-free dashboard with Tailwind CSS.

Include:
- Top Header: Title "Dashboard Summary" and quick action button.
- 3 Large Stat Cards (Total Balance, Active Loans, Next EMI Due).
- Primary Action Card: Large "Apply for New Loan →" button.
"""


# ==========================================================
# LOAN
# ==========================================================

RICH_LOAN_FORM = f"""
{COMMON_RULES}

Generate a comprehensive loan portal for calm users.

Include:
- Applicant Name, Monthly Income, Annual Salary
- Interactive Loan Amount slider
- EMI calculator preview card
- Purpose selector dropdown
- Required Document checklist
- Apply Now button
"""


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


WIZARD_LOAN_FORM = f"""
{COMMON_RULES}

Generate a conversational step-by-step loan application wizard for struggling users.

Include:
- Step 1 of 3 progress bar ("Step 1: Enter Loan Amount")
- Large loan amount input with instant approval estimation card
- Extra-large "Continue to Next Step →" button
- High-contrast minimal layout with zero distractions
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

RICH_PROFILE = f"""
{COMMON_RULES}

Generate a comprehensive user profile & settings portal.

Include:
- Avatar badge & Upload button
- Personal Details section (Name, Email, Phone)
- Security & Password settings section
- Notification preferences toggle switches
- Save All Changes button
"""


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


MINIMAL_PROFILE = f"""
{COMMON_RULES}

Generate a simplified distraction-free profile view.

Include:
- Large avatar badge
- Name & Email fields
- Large "Update Profile" button
"""


# ==========================================================
# CONTACT
# ==========================================================

RICH_CONTACT = f"""
{COMMON_RULES}

Generate a full contact support hub.

Include:
- Main Contact Form (Name, Email, Subject, Message)
- Office Location & Working Hours card
- Support Phone & Email quick badges
- Frequently Asked Questions (FAQ) accordion
- Send Message button
"""


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


WIZARD_CONTACT = f"""
{COMMON_RULES}

Generate a conversational step-by-step support wizard for struggling users.

Include:
- Step 1: "What can we help you with?" topic selector
- Step 2: Message input with prominent helper guidance
- Extra-large "Submit Request →" button
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