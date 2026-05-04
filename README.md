# drone-audit

Open-source Python CLI project for **auxiliary** analysis of exported operation files from DJI Agras agricultural drones.

## Status

Version: `0.3.0-alpha`

This is an **alpha experimental** release. Outputs are technical aids only.

## Scope in current version

- Basic CSV ingestion with common aliases.
- Basic KML parsing (`LineString`, `gx:Track`) for route context.
- Optional complementary JSON field data.
- Operational metrics (distance, time, productivity estimates, efficiency slices).
- Heuristic auxiliary classification and diagnostics.
- HTML technical auxiliary report.

## Important limits

- This project does **not** replace technical reports, field inspections, or responsible professional review.
- It does **not** guarantee definitive diagnosis.
- It does **not** provide automatic regulatory validity.
- It does **not** implement raw DJI DAT parsing.
- Raw DJI TXT telemetry logs are not implemented.

Use wording intentionally: this is an **auxiliary technical report**, with **estimated operational diagnosis** and **experimental heuristics**.

## Privacy and secure use

- Keep real files local only.
- Do not publish real coordinates, client/farm/operator names, serials, or identifiable routes.
- Public examples must be synthetic or safely sanitized.

See:
- [SECURITY.md](SECURITY.md)
- [docs/local-real-file-validation.md](docs/local-real-file-validation.md)
- [docs/sanitization.md](docs/sanitization.md)

## Supported vs planned formats

Current support details are in [docs/support-matrix.md](docs/support-matrix.md).
Roadmap/backlog (not yet implemented) is in [docs/roadmap-backlog.md](docs/roadmap-backlog.md).

## Documentation index

- [CONTRIBUTING.md](CONTRIBUTING.md)
- [SECURITY.md](SECURITY.md)
- [docs/support-matrix.md](docs/support-matrix.md)
- [docs/local-real-file-validation.md](docs/local-real-file-validation.md)
- [docs/release-checklist.md](docs/release-checklist.md)
- [docs/sanitization.md](docs/sanitization.md)
- [docs/quality-gates.md](docs/quality-gates.md)
- [docs/roadmap-backlog.md](docs/roadmap-backlog.md)
- [docs/audit-rules.md](docs/audit-rules.md)
- [examples/real_samples/README.md](examples/real_samples/README.md)

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e .
```

## Tests and lint

```bash
pip install -e ".[test]"
pytest -q
ruff check .
```

## Quick run

```bash
PYTHONPATH=src python -m drone_audit.cli --csv examples/sample_flight.csv --area-ha 12.5 --output reports/report_csv.html
```

## Legal and regulatory note

Output is an **auxiliary report for technical review, without automatic regulatory value**.

## License

GNU GPLv3 only. See [LICENSE](LICENSE).


## Diagnose mode

```bash
PYTHONPATH=src python -m drone_audit.cli --csv examples/sample_flight.csv --area-ha 12.5 --output reports/report_csv.html --diagnose
```
