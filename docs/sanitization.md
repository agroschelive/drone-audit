# CSV sanitization

The CSV sanitizer removes privacy-sensitive fields from CSV-like exports and writes a sanitized copy for safer sharing.

## Behavior
- It returns a sanitized copy and does **not** mutate the input file.
- It removes sensitive columns (for example identifiers, keys, and privacy-risk fields).
- It removes coordinates by default.
- With `--fake-coordinates`, added coordinates are synthetic and do not come from the source file.
- Timestamps are normalized by default.
- Sanitization does not automatically guarantee anonymity.
- Users must inspect sanitized output before publication.

## Commands

```bash
PYTHONPATH=src python -m drone_audit.tools.anonymize_csv \
  --input real_export.csv \
  --output sanitized_export.csv
```

```bash
PYTHONPATH=src python -m drone_audit.tools.anonymize_csv \
  --input real_export.csv \
  --output sanitized_export.csv \
  --fake-coordinates
```

## CLI summary fields
- `original_coordinates_removed`
- `synthetic_coordinates_added`
- `timestamps_normalized`
