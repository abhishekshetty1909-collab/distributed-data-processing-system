import json
import logging
import random
import time
from datetime import datetime, timezone
from uuid import uuid4
from confluent_kafka import Producer
from app.config import settings
from app.logging_config import configure_logging

configure_logging()
logger = logging.getLogger("producer")
PRODUCER_RUN_ID = uuid4().hex[:8].upper()

def make_order_event(sequence):
    return {
        "event_id": str(uuid4()), "event_type": "order_created",
        "event_time": datetime.now(timezone.utc).isoformat(),
        "order_id": f"ORD-{PRODUCER_RUN_ID}-{sequence:08d}",
        "customer_id": f"CUS-{random.randint(1, 500):05d}",
        "product_id": f"PRD-{random.randint(1, 40):04d}",
        "quantity": random.randint(1, 5),
        "unit_price": round(random.uniform(99, 4999), 2),
        "currency": "INR", "status": "created",
    }

def main():
    producer = Producer({
        "bootstrap.servers": settings.kafka_bootstrap_servers,
        "client.id": "python-order-event-producer",
        "acks": "all", "enable.idempotence": True,
    })
    sequence = 1
    rate = max(settings.events_per_second, 0.1)
    logger.info("Publishing to %s at approximately %.2f events/sec", settings.kafka_topic, rate)
    try:
        while True:
            event = make_order_event(sequence)
            producer.produce(
                settings.kafka_topic, key=event["order_id"].encode(),
                value=json.dumps(event).encode(),
                callback=lambda err, msg: logger.error("Delivery failed: %s", err) if err else None,
            )
            producer.poll(0)
            if sequence % 100 == 0:
                logger.info("Produced %s events", sequence)
            sequence += 1
            time.sleep(1 / rate)
    except KeyboardInterrupt:
        logger.info("Producer stopping")
    finally:
        producer.flush(10)

if __name__ == "__main__":
    main()
