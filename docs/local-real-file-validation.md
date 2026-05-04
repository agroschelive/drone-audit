# Local real-file validation

## Safety rules
- Keep real files local only.
- Do not commit raw real files.
- Do not commit real coordinates.
- Do not commit identifiable routes.
- Do not commit client/operator/property/equipment identifiers.
- Do not commit tokens, passwords or API keys.
- Use synthetic or safely sanitized examples for public sharing.

## Before running validation
- [ ] Confirm files are stored outside the repository or in ignored private folders.
- [ ] Confirm no real files are staged in git.
- [ ] Confirm coordinates and timestamps are treated as sensitive.
- [ ] Confirm output files are reviewed before sharing.
- [ ] Confirm generated reports do not contain real coordinates or identifiable routes before publication.

## CSV validation checklist
- [ ] Confirm parser reads the file without crashing.
- [ ] Confirm recognized columns.
- [ ] Confirm missing columns.
- [ ] Confirm warnings.
- [ ] Confirm generated metrics make sense only as auxiliary estimates.
- [ ] Confirm sanitized output removes sensitive data before sharing.
- [ ] Run the anonymization CLI before sharing CSV-like data.

```bash
PYTHONPATH=src python -m drone_audit.cli \
  --csv path/to/local/file.csv \
  --area-ha 12.5 \
  --output reports/local_report.html \
  --diagnose
```

```bash
PYTHONPATH=src python -m drone_audit.tools.anonymize_csv \
  --input path/to/local/file.csv \
  --output sanitized_export.csv
```

```bash
PYTHONPATH=src python -m drone_audit.tools.anonymize_csv \
  --input path/to/local/file.csv \
  --output sanitized_export.csv \
  --fake-coordinates
```

## KML validation checklist
- [ ] Confirm route loads.
- [ ] Confirm map/report generation works.
- [ ] Confirm route is not committed or shared publicly.
- [ ] Confirm any public sample is synthetic.
- [ ] Confirm no real route shape is published.

## DAT/TXT note
- DAT/TXT parsing is not implemented.
- DAT/TXT files must not be uploaded to GitHub.
- Future DAT/TXT support requires locally validated files, tests and documentation.
- Do not add DAT/TXT placeholders.
