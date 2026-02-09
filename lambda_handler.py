import json
from intent_handler import handle_event

def handler(event, context):
    result = handle_event(event)

    # Explicit logging for observability
    print("INTENT EVALUATION RESULT:")
    print(json.dumps(result, indent=2))

    return result