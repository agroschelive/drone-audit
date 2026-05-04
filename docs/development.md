# drone-audit development

## Development setup

```bash
python -m venv .venv
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

## Run tests

```bash
pytest -q
```

## Run lint checks

```bash
ruff check src tests
```

## Run coverage

```bash
pytest -q --cov=drone_audit --cov-report=term-missing
```

## Real data security

Never commit real data. Use synthetic samples whenever possible. Use the anonymization CLI before sharing CSV-like data publicly. Avoid publishing KML routes from real properties, and do not upload DAT files to GitHub.

See also:
- [SECURITY.md](../SECURITY.md)
- [docs/expected-real-files.md](expected-real-files.md)
- [docs/audit-rules.md](audit-rules.md)
