CREATE OR REPLACE VIEW product_revenue AS
SELECT product_id, SUM(quantity) AS units_sold,
       SUM(quantity * unit_price)::NUMERIC(18,2) AS gross_revenue
FROM orders_raw GROUP BY product_id;

CREATE OR REPLACE VIEW customer_value AS
SELECT customer_id, COUNT(DISTINCT order_id) AS order_count,
       SUM(quantity * unit_price)::NUMERIC(18,2) AS gross_spend
FROM orders_raw GROUP BY customer_id;
