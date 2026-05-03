.PHONY: install test lint coverage diagnose

install:
	python -m pip install --upgrade pip
	python -m pip install -e ".[dev]"

test:
	pytest -q

lint:
	ruff check src tests

coverage:
	pytest -q --cov=drone_audit --cov-report=term-missing

diagnose:
	PYTHONPATH=src python -m drone_audit.cli --csv examples/sample_flight.csv --area-ha 12.5 --output reports/report_csv.html --diagnose
