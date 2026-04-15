from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any
import math
import uuid

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

    return {
        "title": "Query results",
        "columns": cols,
        "rows": rows,
        "totals": _rollup_numeric_columns(cols, rows),
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
    if t:
        parts = [f"{k}={_format_cli_scalar(v)}" for k, v in t.items()]
        print("\nTotals (rolled up): " + ", ".join(parts))


def _json_value(v: Any) -> Any:
    if v is None:
        return None
    if isinstance(v, Decimal):
        return float(v)
    if isinstance(v, (datetime, date)):
        return v.isoformat()
    if isinstance(v, uuid.UUID):
        return str(v)
    if isinstance(v, bytes):
        return v.decode("utf-8", errors="replace")
    if hasattr(v, "item") and callable(v.item):
        try:
            return _json_value(v.item())
        except (AttributeError, TypeError, ValueError):
            return str(v)
    return v


def _as_finite_number(v: Any) -> float | None:
    if isinstance(v, bool):
        return None
    if isinstance(v, int):
        return float(v)
    if isinstance(v, float):
        return v if math.isfinite(v) else None
    return None


def _is_non_additive_column(name: str) -> bool:
    """Skip MIN/MAX/AVG-style fields when rolling up row totals (sums are misleading)."""
    n = name.lower()
    if n.startswith(("min_", "max_", "avg_", "mean_", "median_", "std_", "stdev_")):
        return True
    return n.endswith(("_min", "_max", "_avg", "_mean", "_median", "_std", "_stdev"))


def _rollup_numeric_columns(columns: list[str], rows: list[dict[str, Any]]) -> dict[str, int | float]:
    """Sum each additive column where every cell is a finite int or float (after JSON prep)."""
    totals: dict[str, int | float] = {}
    for c in columns:
        if _is_non_additive_column(c):
            continue
        nums: list[float] = []
        for r in rows:
            n = _as_finite_number(r.get(c))
            if n is None:
                nums = []
                break
            nums.append(n)
        if not nums:
            continue
        s = sum(nums)
        if all(_is_int_like(x) for x in nums) and float(s).is_integer():
            totals[c] = int(s)
        else:
            totals[c] = s
    return totals


def _is_int_like(x: float) -> bool:
    return abs(x - round(x)) < 1e-9


def _format_cli_scalar(v: Any) -> str:
    if isinstance(v, float):
        return f"{v:,.2f}"
    if isinstance(v, int):
        return f"{v:,}"
    return str(v)


def _read_sql(name: str) -> str:
    path = SQL_DIR / name
    return path.read_text(encoding="utf-8")


if __name__ == "__main__":
    main()
