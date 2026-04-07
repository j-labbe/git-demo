-- Demo schema: small training dataset for Git/SQL diffs.
DROP TABLE IF EXISTS commits;
CREATE TABLE commits (
    id INTEGER PRIMARY KEY,
    author TEXT NOT NULL,
    message TEXT NOT NULL,
    lines_changed INTEGER NOT NULL DEFAULT 0
);

INSERT INTO commits VALUES
    (1, 'alex', 'Add DuckDB connection', 42),
    (2, 'alex', 'Document uv workflow', 18),
    (3, 'sam', 'Fix typo in README', 3);
