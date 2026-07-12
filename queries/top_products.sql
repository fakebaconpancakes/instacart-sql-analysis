SELECT 
    p.product_name,
    COUNT(op.order_id) as total_orders
FROM order_products__prior op
JOIN products p ON op.product_id = p.product_id
GROUP BY p.product_name
ORDER BY total_orders DESC
LIMIT 10;