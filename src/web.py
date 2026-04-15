"""HTTP server: JSON API + static UI for sales aggregation."""

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse

from src.demo import load_aggregation

ROOT = Path(__file__).resolve().parent.parent
STATIC_DIR = ROOT / "static"

app = FastAPI(title="Sales demo")


@app.get("/api/summary")
def api_summary() -> dict:
    return load_aggregation()


@app.get("/")
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")
