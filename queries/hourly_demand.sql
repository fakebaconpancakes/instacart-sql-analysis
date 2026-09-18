SELECT 
    order_hour_of_day, 
    COUNT(order_id) AS total_orders
FROM orders
GROUP BY order_hour_of_day
ORDER BY order_hour_of_day;