# drone-audit architecture

## Architecture goal

The `drone-audit` architecture should remain simple, testable, and modular while the project evolves toward supporting real DJI Agras ecosystem files.

## Current flow

input (`.csv`/`.kml`/`.json`) -> parser -> normalized dataframe -> pipeline -> metrics -> HTML report / diagnostic JSON

## Parser contract

Each parser should evolve to return:
- normalized dataframe mapped to the project schema;
- warnings;
- source type.

Support for `.dat` and `.txt` files should only be implemented when real files are available for validation.

## Normalized schema

Expected columns:
- timestamp
- latitude
- longitude
- altitude_m
- speed_m_s
- valve_open
- battery_pct
- source
- state

Not every file will provide every column in every situation.

## Metrics

Current metrics:
- distance_m
- time_s
- area_ha
- productivity_ha_h
- state_durations_s

Technical interpretation remains auxiliary and experimental.

## Future architecture steps

- parser registry
- operational state machine
- real TXT parser
- real DAT research/parser
- richer data quality report
- anonymization/sanitization tool for real files
- comparison between productive and non-productive time

## Current classifier role and limitations

The current classifier is a heuristic helper for estimated operational states. It is not definitive proof of aircraft condition, operational compliance, or real spraying activity.
