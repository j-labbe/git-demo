SELECT
    u.first_name || ' ' || u.last_name AS name,
    COUNT(s.id) AS orders,
    SUM(s.amount) AS revenue
FROM users u
JOIN sales s ON s.userId = u.userId
GROUP BY u.userId
ORDER BY orders DESC, revenue DESC;
