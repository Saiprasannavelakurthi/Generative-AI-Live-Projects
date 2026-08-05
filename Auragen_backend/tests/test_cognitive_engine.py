from services.cognitive_engine import cognitive_engine


def test_click_activity():

    events = [
        {
            "type": "click"
        }
    ]

    result = cognitive_engine.calculate_score(events)

    assert result["score"] == 0.5
    assert result["high_load"] is False


def test_move_activity():

    events = [
        {
            "type": "move",
            "velocity": 25,
            "acceleration": 40,
            "hesitation": False
        }
    ]

    result = cognitive_engine.calculate_score(events)

    assert result["score"] == 0.7
    assert result["high_load"] is False


def test_move_with_hesitation():

    events = [
        {
            "type": "move",
            "velocity": 25,
            "acceleration": 40,
            "hesitation": True
        }
    ]

    result = cognitive_engine.calculate_score(events)

    assert result["score"] == 2.2
    assert result["high_load"] is False


def test_high_cognitive_load():

    events = []

    for _ in range(60):

        events.append(
            {
                "type": "move",
                "velocity": 100,
                "acceleration": 100,
                "hesitation": True
            }
        )

    result = cognitive_engine.calculate_score(events)

    assert result["high_load"] is True