-- Example analytical query (good file to branch on for training).
SELECT
SELECT author, SUM(lines_changed) AS total_lines
FROM commits
GROUP BY author
ORDER BY total_lines DESC;
