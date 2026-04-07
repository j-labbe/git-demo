# DuckDB + Python demo

Small **uv** project for Git and coding-agent training: SQL lives under `sql/`, the app lives in `src/demo.py`, and DuckDB persists to `data/demo.duckdb` (create locally; not committed).

```bash
uv sync
uv run python -m src.demo
```

The database file is gitignored; rerun the script to rebuild from `sql/01_schema.sql`.
