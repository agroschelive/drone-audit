# Audit rules

Current operational state classification is heuristic and experimental.

## Current state model

The current classifier uses `speed_m_s` and `valve_open` when available.

States:
- `estimated_spraying`
- `moving`
- `idle`

## Rule summary

- `estimated_spraying`: `valve_open` is true and speed is above the configured spray speed threshold.
- `moving`: speed is above the configured moving threshold when spraying is not detected.
- `idle`: speed is below the configured moving threshold, or data is missing/invalid.

## Limitations

These rules are heuristic and experimental. They are not proof of real spraying/application and must not be interpreted as definitive aircraft, operation, or spraying diagnosis.

Future rule changes must be documented before being treated as reliable. Any rule change must include tests and preserve existing behavior unless explicitly stated.
