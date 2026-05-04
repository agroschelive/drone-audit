# Contributing

## Development environment

```bash
python -m venv .venv
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

## Run quality checks

```bash
ruff check src tests
pytest -q
pytest -q --cov=drone_audit --cov-report=term-missing
```

## Open a pull request

1. Create a topic branch from `main`.
2. Keep changes focused and add or update tests.
3. Preserve existing behavior unless your PR explicitly documents intended behavior changes.
4. Describe scope, limitations, and testing in the PR.

## Contribution rules

- Never commit real client, operator, property, or location data.
- Do not implement DAT support without real validated files and tests.
- Keep the project alpha and experimental.
- Preserve current behavior unless the PR explicitly states otherwise.
