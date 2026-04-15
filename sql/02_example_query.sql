-- Example analytical query (good file to branch on for training).
SELECT
    product,
    COUNT(*) AS line_items,
    COUNT(DISTINCT region) AS regions_sold,
    SUM(amount) AS revenue,
    MIN(amount) AS min_sale,
    MAX(amount) AS max_sale
FROM sales
GROUP BY product
ORDER BY revenue DESC;
