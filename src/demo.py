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

    print(" ".join(cols))
    for row in rows:
        print(" ".join(str(v) for v in row))


def _read_sql(name: str) -> str:
    path = SQL_DIR / name
    return path.read_text(encoding="utf-8")


if __name__ == "__main__":
    main()
