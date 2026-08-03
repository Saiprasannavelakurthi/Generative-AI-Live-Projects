from services.cognitive_engine import cognitive_engine


def test_normal_activity():

    events = [
        {
            "type": "click"
        }
    ]

    result = cognitive_engine.calculate_score(events)

    assert result["score"] == 10
    assert result["high_load"] is False


def test_hesitation():

    events = [
        {
            "type": "hesitation",
            "durationMs": 2000
        }
    ]

    result = cognitive_engine.calculate_score(events)

    assert result["score"] == 20


def test_high_cognitive_load():

    events = [
        {"type": "hesitation"},
        {"type": "hesitation"},
        {"type": "hesitation"},
        {"type": "hesitation"}
    ]

    result = cognitive_engine.calculate_score(events)

    assert result["score"] == 80
    assert result["high_load"] is True