import logging
import time
import psycopg
from psycopg.errors import OperationalError
from app.config import settings

logger = logging.getLogger(__name__)

def connect_with_retry(attempts=12, delay=2.0):
    last_error = None
    for attempt in range(1, attempts + 1):
        try:
            return psycopg.connect(settings.postgres_dsn)
        except OperationalError as exc:
            last_error = exc
            logger.warning("PostgreSQL connection attempt %s/%s failed: %s", attempt, attempts, exc)
            time.sleep(delay)
    raise RuntimeError("Could not connect to PostgreSQL") from last_error

def persist_order(conn, event):
    # Insert and update aggregate atomically. Duplicate event IDs are harmless.
    with conn.transaction():
        row = conn.execute(
            """INSERT INTO orders_raw
            (event_id,event_type,event_time,order_id,customer_id,product_id,quantity,unit_price,currency,status)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (event_id) DO NOTHING RETURNING order_id""",
            (event["event_id"], event["event_type"], event["event_time"], event["order_id"],
             event["customer_id"], event["product_id"], event["quantity"], event["unit_price"],
             event["currency"], event["status"]),
        ).fetchone()
        if row is None:
            return False
        conn.execute(
            """INSERT INTO daily_sales_summary(order_date,currency,order_count,gross_revenue)
            VALUES (%s::date,%s,1,%s)
            ON CONFLICT(order_date,currency) DO UPDATE
            SET order_count=daily_sales_summary.order_count+1,
                gross_revenue=daily_sales_summary.gross_revenue+EXCLUDED.gross_revenue,
                updated_at=NOW()""",
            (event["event_time"], event["currency"], event["quantity"] * event["unit_price"]),
        )
        return True
