-- Example analytical query (good file to branch on for training).
SELECT
    region,
    COUNT(*) AS orders,
    SUM(amount) AS revenue,
    ROUND(AVG(amount), 2) AS avg_order_value
FROM sales
GROUP BY region
ORDER BY revenue DESC;
