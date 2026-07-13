SELECT 
    p.product_name,
    prs.total_purchases,
    prs.total_reorders,
    ROUND((prs.total_reorders * 100.0) / prs.total_purchases, 2) AS reorder_rate_percent
FROM product_reorder_stats prs
JOIN products p ON prs.product_id = p.product_id
WHERE prs.total_purchases > 25000
ORDER BY reorder_rate_percent DESC, total_purchases DESC
LIMIT 15;