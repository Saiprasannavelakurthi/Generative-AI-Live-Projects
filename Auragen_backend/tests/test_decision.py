from services.decision_engine import decision_engine


# =====================================================
# Login Page
# =====================================================

def test_login_low_score():

    ui = decision_engine.decide_ui(
        score=2,
        page_name="login"
    )

    assert ui == "simple_login"


def test_login_medium_score():

    ui = decision_engine.decide_ui(
        score=5,
        page_name="login"
    )

    assert ui == "dashboard"


def test_login_high_score():

    ui = decision_engine.decide_ui(
        score=8,
        page_name="login"
    )

    assert ui == "minimal_login"


# =====================================================
# Dashboard
# =====================================================

def test_dashboard_low_score():

    ui = decision_engine.decide_ui(
        score=2,
        page_name="dashboard"
    )

    assert ui == "rich_dashboard"


def test_dashboard_high_score():

    ui = decision_engine.decide_ui(
        score=8,
        page_name="dashboard"
    )

    assert ui == "minimal_dashboard"


# =====================================================
# Registration
# =====================================================

def test_registration():

    ui = decision_engine.decide_ui(
        score=3,
        page_name="register"
    )

    assert ui == "registration_form"


# =====================================================
# Loan Page
# =====================================================

def test_salary_helper():

    ui = decision_engine.decide_ui(
        score=5,
        page_name="loan",
        active_field="salary"
    )

    assert ui == "loan_salary_helper"


def test_income_helper():

    ui = decision_engine.decide_ui(
        score=5,
        page_name="loan",
        active_field="income"
    )

    assert ui == "loan_income_helper"


def test_minimal_loan():

    ui = decision_engine.decide_ui(
        score=8,
        page_name="loan"
    )

    assert ui == "minimal_loan_form"


# =====================================================
# User Actions
# =====================================================

def test_scrolling():

    ui = decision_engine.decide_ui(
        score=5,
        user_action="scrolling"
    )

    assert ui == "compact_layout"


def test_typing():

    ui = decision_engine.decide_ui(
        score=5,
        user_action="typing"
    )

    assert ui == "form_layout"


def test_clicking():

    ui = decision_engine.decide_ui(
        score=5,
        user_action="clicking"
    )

    assert ui == "interactive_layout"


# =====================================================
# Default
# =====================================================

def test_default_high_score():

    ui = decision_engine.decide_ui(
        score=8
    )

    assert ui == "minimal_ui"