.PHONY: run web ui install
run:
	uv run python -m src.demo

web:
	uv run uvicorn src.web:app --reload --host 127.0.0.1 --port 8000

install:
	uv sync
	
ui:
	duckdb -ui data/demo.duckdb