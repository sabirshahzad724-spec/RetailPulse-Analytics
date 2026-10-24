USE retailpulse;

-- 1. Monthly recognized revenue and order volume
SELECT DATE_FORMAT(order_date, '%Y-%m') AS month,
       SUM(recognized_revenue) AS recognized_revenue,
       COUNT(DISTINCT order_id) AS order_count
FROM retail_orders
GROUP BY DATE_FORMAT(order_date, '%Y-%m')
ORDER BY month;

-- 2. Top 10 products by recognized revenue (delivered revenue is already zero otherwise)
SELECT product_name, SUM(recognized_revenue) AS revenue,
       SUM(CASE WHEN order_status = 'Delivered' THEN quantity ELSE 0 END) AS units_delivered
FROM retail_orders
GROUP BY product_name
ORDER BY revenue DESC
LIMIT 10;

-- 3. Return and cancellation rates by category
SELECT category,
       COUNT(*) AS total_orders,
       SUM(order_status = 'Returned') AS returned_orders,
       ROUND(100 * SUM(order_status = 'Returned') / COUNT(*), 2) AS return_rate_pct,
       SUM(order_status = 'Cancelled') AS cancelled_orders,
       ROUND(100 * SUM(order_status = 'Cancelled') / COUNT(*), 2) AS cancellation_rate_pct
FROM retail_orders
GROUP BY category
ORDER BY return_rate_pct DESC;

-- 4. Channel performance: revenue, delivered order count, average order value
SELECT sales_channel,
       SUM(recognized_revenue) AS revenue,
       SUM(order_status = 'Delivered') AS delivered_orders,
       ROUND(SUM(recognized_revenue) / NULLIF(SUM(order_status = 'Delivered'), 0), 2) AS aov
FROM retail_orders
GROUP BY sales_channel
ORDER BY revenue DESC;

-- 5. Revenue concentration by customer segment
WITH segment_revenue AS (
    SELECT customer_segment, SUM(recognized_revenue) AS revenue
    FROM retail_orders
    GROUP BY customer_segment
)
SELECT customer_segment, revenue,
       ROUND(100 * revenue / NULLIF(SUM(revenue) OVER (), 0), 2) AS revenue_share_pct
FROM segment_revenue
ORDER BY revenue DESC;

-- 6. Customers with at least 3 delivered orders and their lifetime recognized revenue
SELECT customer_id,
       COUNT(DISTINCT order_id) AS delivered_orders,
       SUM(recognized_revenue) AS lifetime_revenue
FROM retail_orders
WHERE order_status = 'Delivered'
GROUP BY customer_id
HAVING COUNT(DISTINCT order_id) >= 3
ORDER BY lifetime_revenue DESC;

-- 7. Discount band comparison (revenue only; no cost/margin data is available)
SELECT CASE
         WHEN discount_pct = 0 THEN '0%'
         WHEN discount_pct <= 10 THEN '1-10%'
         ELSE '11%+'
       END AS discount_band,
       COUNT(*) AS order_count,
       SUM(recognized_revenue) AS revenue
FROM retail_orders
GROUP BY discount_band
ORDER BY revenue DESC;

-- 8. Data-quality check: duplicate order IDs (should return no rows if primary key was enforced)
SELECT order_id, COUNT(*) AS duplicate_count
FROM retail_orders
GROUP BY order_id
HAVING COUNT(*) > 1;
