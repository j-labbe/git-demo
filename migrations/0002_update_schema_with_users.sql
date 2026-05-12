-- Migration number: 0002 	 2026-05-12T17:34:49.274Z
DROP TABLE IF EXISTS sales;
DROP TABLE IF EXISTS users;


CREATE TABLE users (
    userId INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL
);

CREATE TABLE sales (
    id INTEGER PRIMARY KEY,
    region TEXT NOT NULL,
    product TEXT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    userId INTEGER NOT NULL,
    FOREIGN KEY (userId) REFERENCES users(userId) ON DELETE CASCADE
);

INSERT INTO users VALUES
    (1, 'Udbhav', 'Pangotra'),
    (2, 'Lovepreet', 'Singh'),
    (3, 'Hitesh', 'Chheda'),
    (4, 'Ben', 'Potts');

INSERT INTO sales VALUES
    (1, 'West', 'Widget', 199.00, 1),
    (2, 'West', 'Gadget', 45.50, 2),
    (3, 'East', 'Widget', 210.00, 4),
    (4, 'East', 'Service plan', 89.99, 3),
    (5, 'Central', 'Gadget', 52.00, 4),
    (6, 'West', 'Widget', 199.00, 1);

