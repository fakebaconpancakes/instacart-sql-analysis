WITH product_reorder_stats AS (
    SELECT 
        p.product_id,
        p.product_name,
        COUNT(op.order_id) AS total_orders,
        SUM(op.reordered) AS total_reorders,
        ROUND(AVG(op.reordered) * 100, 2) AS reorder_rate_percent
    FROM order_products__prior op
    JOIN products p ON op.product_id = p.product_id
    GROUP BY p.product_id, p.product_name
    HAVING COUNT(op.order_id) >= 100
)
SELECT 
    product_name,
    total_orders,
    total_reorders,
    reorder_rate_percent
FROM product_reorder_stats
ORDER BY reorder_rate_percent DESC
LIMIT 10;