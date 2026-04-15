from __future__ import annotations

from decimal import Decimal
from pathlib import Path
from typing import Any

import duckdb

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
DB_PATH = DATA_DIR / "demo.duckdb"
SQL_DIR = ROOT / "sql"


def load_aggregation() -> dict[str, Any]:
    """Run schema + aggregation query; return JSON-serializable summary."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    schema_sql = _read_sql("01_schema.sql")
    query_sql = _read_sql("02_example_query.sql")

    conn = duckdb.connect(str(DB_PATH))
    try:
        conn.execute(schema_sql)
        conn.execute(query_sql)
        cols = [d[0] for d in (conn.description or [])]
        raw_rows = conn.fetchall()
    finally:
        conn.close()

    rows: list[dict[str, Any]] = []
    for tup in raw_rows:
        row: dict[str, Any] = {}
        for i, c in enumerate(cols):
            row[c] = _json_value(tup[i])
        rows.append(row)

    total_orders = sum(int(r["orders"]) for r in rows)
    total_revenue = sum(float(r["revenue"]) for r in rows)

    return {
        "title": "Aggregation: sales by region",
        "columns": cols,
        "rows": rows,
        "totals": {"orders": total_orders, "revenue": total_revenue},
    }


def main() -> None:
    data = load_aggregation()
    cols = data["columns"]
    rows_tuples = [tuple(r[c] for c in cols) for r in data["rows"]]

    print(f"{data['title']}\n")
    col_widths = [max(len(c), max((len(str(r[i])) for r in rows_tuples), default=0)) for i, c in enumerate(cols)]
    header = "  ".join(c.ljust(col_widths[i]) for i, c in enumerate(cols))
    print(header)
    print("  ".join("-" * w for w in col_widths))
    for row in rows_tuples:
        print("  ".join(str(v).ljust(col_widths[i]) for i, v in enumerate(row)))

    t = data["totals"]
    print(f"\nTotals (rolled up): {t['orders']} orders, ${t['revenue']:,.2f} revenue")


def _json_value(v: Any) -> Any:
    if isinstance(v, Decimal):
        return float(v)
    return v


def _read_sql(name: str) -> str:
    path = SQL_DIR / name
    return path.read_text(encoding="utf-8")


if __name__ == "__main__":
    main()
