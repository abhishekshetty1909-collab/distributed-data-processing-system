import pytest
from app.events import validate_event

def valid_event():
    return {
        "event_id": "550e8400-e29b-41d4-a716-446655440000",
        "event_type": "order_created", "event_time": "2026-11-16T12:00:00+00:00",
        "order_id": "ORD-1", "customer_id": "CUS-1", "product_id": "PRD-1",
        "quantity": 2, "unit_price": 100.0, "currency": "INR", "status": "created",
    }

def test_valid_event_passes():
    assert validate_event(valid_event())["order_id"] == "ORD-1"

@pytest.mark.parametrize("field,value", [("quantity", 0), ("quantity", -1), ("unit_price", -2), ("currency", "IN")])
def test_invalid_values_fail(field, value):
    event = valid_event()
    event[field] = value
    with pytest.raises(ValueError):
        validate_event(event)

def test_missing_field_fails():
    event = valid_event()
    del event["customer_id"]
    with pytest.raises(ValueError, match="Missing required fields"):
        validate_event(event)

def test_invalid_uuid_fails():
    event = valid_event()
    event["event_id"] = "not-a-uuid"
    with pytest.raises(ValueError, match="UUID"):
        validate_event(event)
