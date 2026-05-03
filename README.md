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

## Installation

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows PowerShell
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
