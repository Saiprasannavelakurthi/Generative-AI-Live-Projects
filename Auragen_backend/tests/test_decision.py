from services.decision_engine import decision_engine


def test_low_score():

    ui = decision_engine.decide_ui(10)
    assert ui == "simple_login"


def test_medium_score():

    ui = decision_engine.decide_ui(40)

    assert ui == "dashboard"


def test_high_score():

    ui = decision_engine.decide_ui(80)

    assert ui == "minimal_ui"