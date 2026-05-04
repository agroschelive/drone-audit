# drone-audit

Open-source, minimal and experimental project for auxiliary analysis of exported operation files from DJI Agras agricultural drones.

The initial goal is to turn simple files, such as KML and CSV, into a basic report with route, distance, time, estimated productivity and optional operational notes.

## Status

Version: `0.2.1-alpha`

This project is still under development. Results must be reviewed before any technical, commercial, operational or regulatory use.

## What works in this version

- Basic KML parsing, including `LineString` and `gx:Track`.
- Basic CSV parsing with common column aliases.
- Traveled distance calculation.
- Total time calculation when timestamps are available.
- Estimated productivity calculation when an area value is provided.
- Simple operational state classification when speed and a valve/spray indicator are available.
- Optional complementary field data in JSON.
- Simple HTML report generation with an embedded map.
- Basic automated tests.

## What this version does not guarantee

- Complete DAT file parsing.
- Automatic SmartFarm integration.
- Compatibility with every DJI export format.
- Definitive automatic identification of real spraying/application.
- Complete technical diagnosis of the aircraft/drone.
- Operational, agronomic, regulatory or legal accuracy.
- Compliance with manufacturer requirements, aviation authorities, agricultural authorities, local laws or operational standards.

## Proper use

`drone-audit` is an auxiliary tool. It does not replace professional interpretation, signed technical reports, field inspection, agronomic validation, regulatory review or decisions made by the responsible technical professional.

Technical decisions remain the responsibility of the operator, engineer, agronomist, consultant, operating company or qualified responsible professional.

See also: [`DISCLAIMER.md`](DISCLAIMER.md).

## Expected inputs

- `.kml` route file.
- `.csv` tabular data file, when available.
- Optional `.json` file with authorized complementary field data.

Never publish real client data, private coordinates, identifiable flight files, property names, tokens, passwords or API keys.


## Data security

Do not publish real client, property, or operator data. Do not publish real coordinates. Public examples must be synthetic or safely sanitized. See [SECURITY.md](SECURITY.md) and [docs/expected-real-files.md](docs/expected-real-files.md).

## Audit rules

Current operational states are heuristic and experimental. Classification rules are documented in [docs/audit-rules.md](docs/audit-rules.md). The project does not provide definitive aircraft, operation, or real spraying diagnosis.


## Project documentation

- [SECURITY.md](SECURITY.md)
- [CONTRIBUTING.md](CONTRIBUTING.md)
- [CHANGELOG.md](CHANGELOG.md)
- [docs/architecture.md](docs/architecture.md)
- [docs/audit-rules.md](docs/audit-rules.md)
- [docs/support-matrix.md](docs/support-matrix.md)
- [docs/sanitization.md](docs/sanitization.md)
- [docs/expected-real-files.md](docs/expected-real-files.md)
- [docs/local-real-file-validation.md](docs/local-real-file-validation.md)
- [docs/release-checklist.md](docs/release-checklist.md)
- [docs/quality-gates.md](docs/quality-gates.md)
- [docs/roadmap-backlog.md](docs/roadmap-backlog.md)

## Alpha readiness

The repository is prepared for safe local validation. Real files must remain local. Public examples must be synthetic or safely sanitized. The project does not provide definitive aircraft, operation or spraying diagnosis.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows PowerShell
python -m pip install --upgrade pip
pip install -e .
```

## Run with KML

```bash
PYTHONPATH=src python -m drone_audit.cli \
  --kml examples/sample_route.kml \
  --area-ha 12.5 \
  --output reports/report_kml.html
```

## Run with CSV

```bash
PYTHONPATH=src python -m drone_audit.cli \
  --csv examples/sample_flight.csv \
  --area-ha 12.5 \
  --output reports/report_csv.html
```

## Run with complementary field data

```bash
PYTHONPATH=src python -m drone_audit.cli \
  --csv examples/sample_flight.csv \
  --field-data examples/sample_field_data.json \
  --area-ha 12.5 \
  --output reports/enriched_report.html
```


## Run in diagnostic mode

```bash
PYTHONPATH=src python -m drone_audit.cli \
  --csv examples/sample_flight.csv \
  --area-ha 12.5 \
  --output reports/report_csv.html \
  --diagnose
```

## Run tests

```bash
pip install -e ".[test]"
pytest -q
```

## Author

Project created and idealized by **Italo Schelive Correia**.

Public contact: agroschelive@gmail.com

## License

This project is distributed under the **GNU General Public License v3.0 only**.

This means the code can be used, studied, modified and redistributed under the terms of GPLv3. Redistributed and modified versions must comply with the same license and keep applicable notices.

See [`LICENSE`](LICENSE), [`NOTICE.md`](NOTICE.md) and [`AUTHORS.md`](AUTHORS.md).

For GitHub publication instructions, see [`docs/github-create-step-by-step.md`](docs/github-create-step-by-step.md).

## Trademark notice

DJI and Agras are trademarks of their respective owners. This project is not affiliated with, sponsored by, approved by or endorsed by DJI. The use of these names is descriptive only, to indicate technical compatibility with exported files from related platforms.

## DJI Agras operational audit foundation (new)

This version adds a foundational layer for operational KPI auditing:

- Operational metrics utilities for time slicing (spraying, maneuvering, moving, idle), operational efficiency, productivity, battery consumption per hectare and real application rate.
- Automatic operational diagnostics with messages for inefficient maneuvering, low spraying time, low efficiency and potential route/refill issues.
- Extended report layout with an operational dashboard and mission summary section.
- A future-ready telemetry importer structure in `src/drone_audit/lib/importers` with generic CSV/JSON parsing and conversion to `eventos_voo` records.
- SQL migration draft in `db/migrations/20260504_operational_audit_schema.sql` containing core entities (`clientes`, `fazendas`, `talhoes`, `operadores`, `drones`, `baterias`, `missoes`, `voos`, `eventos_voo`, etc.).

Note: this repository currently runs as a local Python pipeline/CLI. The SQL migration is prepared for future Supabase/Postgres integration.


## Base Agras

- Formatos aceitos: XLSX, CSV, KML e JSON.
- Origem esperada: DJI SmartFarm / DJI Agriculture Platform (exportação manual).
- Limitações: KML pode não conter telemetria detalhada; algumas métricas podem ser estimadas.
- Métricas calculadas: tempo total, tempo pulverizando/manobrando/deslocando/parado, eficiência operacional, produtividade, consumo bateria/ha e distância/ha.
- Próximos passos: importar XLSX e KML reais, validar aliases de colunas reais, conectar com Supabase Storage e preparar integração autorizada futura.

## Telemetria Agras (experimental)
Suporte adicional para TXT tabular normalizado com sinais `spray_on`, `valve_open`, `pump_on`, `flow_l_min`, `volume_total_l`, `swath_width_m`, `area_total_ha`.
KML pode ter telemetria limitada. DAT bruto DJI/Agras ainda não é suportado; converta localmente para CSV/TXT legível.

