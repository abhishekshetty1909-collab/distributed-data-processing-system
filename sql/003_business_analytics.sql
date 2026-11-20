
-- 003_business_analytics.sql

-- 1. Daily revenue analysis
CREATE OR REPLACE VIEW daily_revenue AS
SELECT
    event_time::date AS sales_date,
    currency,
    COUNT(*) AS total_events,
    COUNT(DISTINCT order_id) AS unique_orders,
    SUM(quantity * unit_price)::NUMERIC(18,2) AS total_revenue
FROM orders_raw
GROUP BY event_time::date, currency;


-- 2. Monthly revenue analysis
CREATE OR REPLACE VIEW monthly_revenue AS
SELECT
    DATE_TRUNC('month', event_time)::date AS sales_month,
    currency,
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(quantity * unit_price)::NUMERIC(18,2) AS total_revenue
FROM orders_raw
GROUP BY DATE_TRUNC('month', event_time), currency;


-- 3. Product performance
CREATE OR REPLACE VIEW product_performance AS
SELECT
    product_id,
    SUM(quantity) AS units_sold,
    COUNT(DISTINCT order_id) AS unique_orders,
    SUM(quantity * unit_price)::NUMERIC(18,2) AS revenue,
    RANK() OVER (
        ORDER BY SUM(quantity * unit_price) DESC
    ) AS revenue_rank
FROM orders_raw
GROUP BY product_id;


-- 4. Customer analytics
CREATE OR REPLACE VIEW customer_analytics AS
SELECT
    customer_id,
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(quantity * unit_price)::NUMERIC(18,2) AS total_spend,
    AVG(quantity * unit_price)::NUMERIC(18,2) AS avg_line_value
FROM orders_raw
GROUP BY customer_id;


-- 5. Overall sales KPIs
CREATE OR REPLACE VIEW sales_kpis AS
SELECT
    COUNT(*) AS total_events,
    COUNT(DISTINCT order_id) AS unique_orders,
    COUNT(DISTINCT customer_id) AS unique_customers,
    SUM(quantity) AS units_sold,
    SUM(quantity * unit_price)::NUMERIC(18,2) AS total_revenue,
    AVG(quantity * unit_price)::NUMERIC(18,2) AS avg_line_value
FROM orders_raw;
