import json
from intent_engine import evaluate_intent


def handle_event(event: dict) -> dict:
    
    detail = event.get("detail", {})

    if not detail:
        raise ValueError("Event missing 'detail' field")

    hypotheses = evaluate_intent(detail)

    return {
        "status": "processed",
        "hypotheses": hypotheses
    }


if __name__ == "__main__":
    # Local test runner for the handler
    with open("test_events.json") as f:
        event = json.load(f)

    result = handle_event(event)

    print("Handler output:")
    print(json.dumps(result, indent=2))