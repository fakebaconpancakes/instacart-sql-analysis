WITH UserMetrics AS (
    SELECT 
        user_id, 
        MAX(order_number) AS total_orders, 
        AVG(days_since_prior_order) AS avg_days_between_orders
    FROM orders
    GROUP BY user_id
),
SegmentedUsers AS (
    SELECT 
        user_id,
        CASE 
            WHEN total_orders > 10 AND avg_days_between_orders < 14 THEN 'Loyal Customer'
            WHEN avg_days_between_orders > 28 THEN 'At Risk'
            ELSE 'Casual Shopper'
        END AS customer_segment
    FROM UserMetrics
)
SELECT 
    customer_segment, 
    COUNT(user_id) as total_users 
FROM SegmentedUsers 
GROUP BY customer_segment
ORDER BY total_users DESC;

