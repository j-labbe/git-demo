-- Demo schema: small sales dataset for Git/SQL diffs.
DROP TABLE IF EXISTS sales;
CREATE TABLE sales (
    id INTEGER PRIMARY KEY,
    region TEXT NOT NULL,
    product TEXT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL
);

INSERT INTO sales VALUES
    (1, 'West', 'Widget', 199.00),
    (2, 'West', 'Gadget', 45.50),
    (3, 'East', 'Widget', 210.00),
    (4, 'East', 'Service plan', 89.99),
    (5, 'Central', 'Gadget', 52.00),
    (6, 'West', 'Widget', 199.00);
