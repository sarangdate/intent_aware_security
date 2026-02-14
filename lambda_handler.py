import json
import boto3
from intent_handler import handle_event

dynamodb = boto3.client("dynamodb")
TABLE_NAME = "intent_engine_idempotency"

def handler(event, context):
    event_id = event.get("detail", {}).get("eventID")

    if not event_id:
        raise ValueError("Missing eventID")

    try:
        dynamodb.put_item(
            TableName=TABLE_NAME,
            Item={"event_id": {"S": event_id}},
            ConditionExpression="attribute_not_exists(event_id)"
        )
    except Exception as e:
        if "ConditionalCheckFailedException" in str(e):
            print(f"Duplicate event ignored: {event_id}")
            return {"status": "duplicate_ignored"}
        else:
            raise

    result = handle_event(event)
    print(json.dumps(result))
    return result