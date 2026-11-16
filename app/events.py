from datetime import datetime
from uuid import UUID

REQUIRED_FIELDS = {
    "event_id", "event_type", "event_time", "order_id", "customer_id",
    "product_id", "quantity", "unit_price", "currency", "status",
}

def validate_event(event):
    missing = REQUIRED_FIELDS - event.keys()
    if missing:
        raise ValueError(f"Missing required fields: {', '.join(sorted(missing))}")
    try:
        UUID(str(event["event_id"]))
    except (ValueError, TypeError, AttributeError) as exc:
        raise ValueError("event_id must be a UUID") from exc
    if event["event_type"] != "order_created":
        raise ValueError("Unsupported event_type")
    try:
        datetime.fromisoformat(str(event["event_time"]).replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("event_time must be an ISO-8601 timestamp") from exc
    if not isinstance(event["quantity"], int) or isinstance(event["quantity"], bool) or event["quantity"] <= 0:
        raise ValueError("quantity must be a positive integer")
    if not isinstance(event["unit_price"], (int, float)) or isinstance(event["unit_price"], bool) or event["unit_price"] < 0:
        raise ValueError("unit_price must be a non-negative number")
    if len(str(event["currency"])) != 3:
        raise ValueError("currency must be a three-letter code")
    return event
