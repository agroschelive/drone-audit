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


## Documentation and safety references

- [docs/quality-gates.md](docs/quality-gates.md)
- [docs/release-checklist.md](docs/release-checklist.md)
- [docs/local-real-file-validation.md](docs/local-real-file-validation.md)
- [docs/sanitization.md](docs/sanitization.md)

Contributors must not attach real files to issues or pull requests. Use synthetic or safely sanitized samples only.
