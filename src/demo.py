from pathlib import Path
import duckdb

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
DB_PATH = DATA_DIR / "demo.duckdb"
SQL_DIR = ROOT / "sql"


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    schema_sql = _read_sql("01_schema.sql")
    query_sql = _read_sql("02_example_query.sql")

    conn = duckdb.connect(str(DB_PATH))
    try:
        conn.execute(schema_sql)
        conn.execute(query_sql)
        cols = [d[0] for d in (conn.description or [])]
        rows = conn.fetchall()
    finally:
        conn.close()

    print("Aggregation: sales by region\n")
    col_widths = [max(len(c), max((len(str(r[i])) for r in rows), default=0)) for i, c in enumerate(cols)]
    header = "  ".join(c.ljust(col_widths[i]) for i, c in enumerate(cols))
    print(header)
    print("  ".join("-" * w for w in col_widths))
    for row in rows:
        print("  ".join(str(v).ljust(col_widths[i]) for i, v in enumerate(row)))

    total_orders = sum(r[1] for r in rows)
    total_revenue = sum(float(r[2]) for r in rows)
    print(f"\nTotals (rolled up): {total_orders} orders, ${total_revenue:,.2f} revenue")


def _read_sql(name: str) -> str:
    path = SQL_DIR / name
    return path.read_text(encoding="utf-8")


if __name__ == "__main__":
    main()
