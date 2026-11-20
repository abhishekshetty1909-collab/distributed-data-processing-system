-- Recreate corrected analytics views

DROP VIEW IF EXISTS sales_kpis;
DROP VIEW IF EXISTS customer_analytics;
DROP VIEW IF EXISTS product_performance;

CREATE VIEW sales_kpis AS
SELECT
    COUNT(*) AS total_orders,
    COUNT(DISTINCT event_id) AS unique_events,
    COUNT(DISTINCT customer_id) AS unique_customers,
    SUM(quantity) AS units_sold,
    SUM(quantity * unit_price)::NUMERIC(18,2) AS total_revenue,
    AVG(quantity * unit_price)::NUMERIC(18,2) AS average_order_value
FROM orders_raw;

CREATE VIEW customer_analytics AS
SELECT
    customer_id,
    COUNT(*) AS total_orders,
    SUM(quantity * unit_price)::NUMERIC(18,2) AS total_spend,
    AVG(quantity * unit_price)::NUMERIC(18,2) AS average_order_value
FROM orders_raw
GROUP BY customer_id;

CREATE VIEW product_performance AS
SELECT
    product_id,
    SUM(quantity) AS units_sold,
    COUNT(*) AS order_events,
    SUM(quantity * unit_price)::NUMERIC(18,2) AS revenue,
    RANK() OVER (
        ORDER BY SUM(quantity * unit_price) DESC
    ) AS revenue_rank
FROM orders_raw
GROUP BY product_id;