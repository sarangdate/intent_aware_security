import json
from intent_engine import evaluate_intent

with open("test_events.json") as f:
    event = json.load(f)

hypotheses = evaluate_intent(event["detail"])

print("Intent evaluation result:")
for h in hypotheses:
    print(h)