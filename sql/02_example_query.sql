SELECT
    region,
    COUNT(*) AS orders,
    SUM(amount) AS revenue,
    ROUND(AVG(amount), 2) AS avg_order_value,
    RANK() OVER (ORDER BY SUM(amount) DESC) AS revenue_rank
FROM sales
GROUP BY region
ORDER BY revenue_rank DESC;
