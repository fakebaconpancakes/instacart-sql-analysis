WITH paired_products AS (
	SELECT 
		op1.product_id AS p1_id,
		op2.product_id AS p2_id,
		COUNT(*) AS frequency
	FROM order_products__prior op1
	JOIN order_products__prior op2 
		ON op1.order_id = op2.order_id 
		AND op1.product_id < op2.product_id
	GROUP BY op1.product_id, op2.product_id
	ORDER BY frequency DESC
	LIMIT 10
)
SELECT 
	prod1.product_name AS product_1,
	prod2.product_name AS product_2,
	pp.frequency AS times_bought_together
FROM paired_products pp
JOIN products prod1 ON pp.p1_id = prod1.product_id
JOIN products prod2 ON pp.p2_id = prod2.product_id
ORDER BY times_bought_together DESC;