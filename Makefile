UV := uv
VENV := .venv
PYTHON := $(VENV)/bin/python

.PHONY: run web ui install

$(PYTHON):
	@test -f "$(PYTHON)" || $(UV) venv "$(VENV)"

install: $(PYTHON)
	$(UV) sync

run: $(PYTHON)
	$(UV) run python -m src.demo

web: $(PYTHON)
	$(UV) run uvicorn src.web:app --reload --host 127.0.0.1 --port 8000

ui: $(PYTHON)
	$(UV) run duckdb -ui data/demo.duckdb
