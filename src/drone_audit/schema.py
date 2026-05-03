"""Normalized telemetry schema used by drone-audit.

Parsers should convert vendor/export-specific names into these normalized columns.
Future DJI Agras parsers should output this schema whenever possible.
Not every source file will provide every column.
"""

from __future__ import annotations

NORMALIZED_COLUMNS = [
    "timestamp",
    "latitude",
    "longitude",
    "altitude_m",
    "speed_m_s",
    "valve_open",
    "battery_pct",
    "source",
    "state",
]

REQUIRED_POSITION_COLUMNS = ["latitude", "longitude"]
OPTIONAL_TELEMETRY_COLUMNS = ["altitude_m", "speed_m_s", "valve_open", "battery_pct"]
