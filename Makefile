VENV := .venv
PYTHON := $(VENV)/bin/python

.PHONY: run web ui install

$(PYTHON):
	@test -f "$(PYTHON)" || uv venv "$(VENV)"

install: $(PYTHON)
	uv sync

run: $(PYTHON)
	uv run python -m src.demo

web: $(PYTHON)
	uv run uvicorn src.web:app --reload --host 127.0.0.1 --port 8000

ui: $(PYTHON)
	uv run duckdb -ui data/demo.duckdb
