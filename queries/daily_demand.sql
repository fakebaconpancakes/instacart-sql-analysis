SELECT 
    order_dow, 
    COUNT(order_id) AS total_orders
FROM orders
GROUP BY order_dow
ORDER BY order_dow;