# Distributed Data Processing System

A portfolio-ready streaming data engineering project using **Python, Apache Kafka, PostgreSQL, Linux, and Docker Compose**.

## Pipeline

```text
Python Producer -> Kafka topic (orders) -> Python Consumer -> PostgreSQL
     |                    |                    |               |
 Generate JSON       Buffer/partitions     Validate +       orders_raw
 order events        consumer group        idempotent write daily_sales_summary
```

The producer creates synthetic e-commerce order events. Kafka buffers them in the `orders` topic. The consumer validates each event and persists it to PostgreSQL. A transaction inserts the raw event and updates a daily revenue aggregate. The unique event UUID prevents duplicate database rows on Kafka replay.

## Run it

Prerequisites: Docker Desktop/Engine with Docker Compose v2 and Git.

```bash
 git clone https://github.com/YOUR-USERNAME/distributed-data-processing-system.git
 cd distributed-data-processing-system
 cp .env.example .env
 docker compose up --build -d
 docker compose ps
 docker compose logs -f producer consumer
```

Inspect stored events:

```bash
docker compose exec postgres psql -U pipeline -d ecommerce -c "SELECT order_id, customer_id, product_id, quantity, unit_price, event_time FROM orders_raw ORDER BY ingested_at DESC LIMIT 10;"
```

Inspect aggregates:

```bash
docker compose exec postgres psql -U pipeline -d ecommerce -c "SELECT * FROM daily_sales_summary ORDER BY order_date DESC LIMIT 10;"
```

Stop containers with `docker compose down`. Remove containers and demo data with `docker compose down -v`.

## Structure

```text
app/       Python producer, consumer, validation, DB and configuration
sql/       PostgreSQL schema and analytics views
scripts/   Linux shell launch scripts
tests/     pytest unit tests
Dockerfile Python application image
docker-compose.yml Kafka, PostgreSQL and app orchestration
.env.example example local configuration
Makefile   common development commands
```

## Example event

```json
{
  "event_id": "550e8400-e29b-41d4-a716-446655440000",
  "event_type": "order_created",
  "event_time": "2026-11-16T12:00:00+00:00",
  "order_id": "ORD-00000001",
  "customer_id": "CUS-00042",
  "product_id": "PRD-0012",
  "quantity": 2,
  "unit_price": 499.0,
  "currency": "INR",
  "status": "created"
}
```

## Database objects

- `orders_raw`: one row per unique source event; `event_id` is the primary key.
- `daily_sales_summary`: daily order count and gross revenue by currency.
- `product_revenue`: product-level units sold and revenue view.
- `customer_value`: customer-level order count and spend view.

Example queries:

```sql
SELECT product_id, SUM(quantity * unit_price) AS revenue
FROM orders_raw GROUP BY product_id ORDER BY revenue DESC;

SELECT order_date, order_count, gross_revenue
FROM daily_sales_summary ORDER BY order_date;

SELECT * FROM product_revenue ORDER BY gross_revenue DESC;
```

## Tests

```bash
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
pytest -q
```

## Engineering decisions

- Producer enables Kafka idempotence and uses `acks=all`.
- Consumer disables auto-commit and commits offsets only after successful database persistence.
- PostgreSQL transactions insert the event and update the aggregate atomically.
- Unique `event_id` makes database writes idempotent if a message is replayed.
- Three Kafka partitions support consumer-group scaling; add partitions before scaling consumers beyond the partition count.
- Invalid messages are logged and skipped in this demo. A production extension should publish them to a dead-letter topic.
- Demo credentials and plaintext local networking are for development only. Production needs secrets management, TLS, authentication, monitoring, schema evolution and retention policies.

## Resume description

**Distributed Data Processing System | Python, Apache Kafka, PostgreSQL, Linux, Docker**

- Built an event-driven data pipeline using Python and Apache Kafka to ingest and process synthetic e-commerce order events.
- Developed producer and consumer services with JSON validation, partition keys, consumer groups and idempotent PostgreSQL writes.
- Designed PostgreSQL tables, analytical views and incremental daily revenue aggregates for SQL-based reporting.
- Containerized the pipeline using Docker Compose and added Linux shell scripts, structured logging, health checks and automated tests.

Do not claim throughput or production-scale performance until you benchmark your own environment.
