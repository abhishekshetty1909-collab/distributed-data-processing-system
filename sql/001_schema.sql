CREATE TABLE IF NOT EXISTS orders_raw (
    event_id UUID PRIMARY KEY,
    event_type TEXT NOT NULL,
    event_time TIMESTAMPTZ NOT NULL,
    order_id TEXT NOT NULL,
    customer_id TEXT NOT NULL,
    product_id TEXT NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(12,2) NOT NULL CHECK (unit_price >= 0),
    currency CHAR(3) NOT NULL,
    status TEXT NOT NULL,
    ingested_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_orders_event_time ON orders_raw(event_time);
CREATE INDEX IF NOT EXISTS idx_orders_product_id ON orders_raw(product_id);
CREATE INDEX IF NOT EXISTS idx_orders_customer_id ON orders_raw(customer_id);

CREATE TABLE IF NOT EXISTS daily_sales_summary (
    order_date DATE NOT NULL,
    currency CHAR(3) NOT NULL,
    order_count BIGINT NOT NULL DEFAULT 0,
    gross_revenue NUMERIC(18,2) NOT NULL DEFAULT 0,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY(order_date,currency)
);
