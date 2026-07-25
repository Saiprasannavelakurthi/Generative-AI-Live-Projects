from services.decision_engine import decision_engine

print("Score 20 ->", decision_engine.decide_ui(20))
print("Score 50 ->", decision_engine.decide_ui(50))
print("Score 90 ->", decision_engine.decide_ui(90))