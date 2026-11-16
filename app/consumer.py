import json
import logging
import time
from confluent_kafka import Consumer
from app.config import settings
from app.db import connect_with_retry, persist_order
from app.events import validate_event
from app.logging_config import configure_logging

configure_logging()
logger = logging.getLogger("consumer")

def main():
    conn = connect_with_retry()
    consumer = Consumer({
        "bootstrap.servers": settings.kafka_bootstrap_servers,
        "group.id": settings.kafka_group_id,
        "auto.offset.reset": "earliest",
        "enable.auto.commit": False,
        "max.poll.interval.ms": 300000,
    })
    consumer.subscribe([settings.kafka_topic])
    logger.info("Subscribed to %s", settings.kafka_topic)
    processed = 0
    try:
        while True:
            message = consumer.poll(1.0)
            if message is None:
                continue
            if message.error():
                logger.error("Kafka error: %s", message.error())
                continue
            try:
                event = validate_event(json.loads(message.value().decode("utf-8")))
                inserted = persist_order(conn, event)
                # Commit only after the database transaction succeeds.
                consumer.commit(message=message, asynchronous=False)
                if inserted:
                    processed += 1
                    if processed % 100 == 0:
                        logger.info("Persisted %s new events", processed)
            except (ValueError, json.JSONDecodeError, UnicodeDecodeError) as exc:
                # Demo behavior: log and skip. Production should use a dead-letter topic.
                logger.exception("Invalid event at offset %s: %s", message.offset(), exc)
                consumer.commit(message=message, asynchronous=False)
            except Exception:
                logger.exception("Persistence failed; offset remains uncommitted")
                time.sleep(2)
    except KeyboardInterrupt:
        logger.info("Consumer stopping")
    finally:
        consumer.close()
        conn.close()

if __name__ == "__main__":
    main()
