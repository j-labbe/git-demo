.PHONY: run ui install
run:
	uv run python -m src.demo

install:
	uv sync
	
ui:
	duckdb -ui data/demo.duckdb