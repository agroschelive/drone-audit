"""Normalized telemetry schema used by drone-audit."""
from __future__ import annotations

NORMALIZED_COLUMNS = [
    "timestamp", "latitude", "longitude", "altitude_m", "speed_m_s", "heading_deg",
    "battery_pct", "voltage_v", "current_a", "spray_on", "valve_open", "pump_on",
    "flow_l_min", "volume_total_l", "swath_width_m", "area_total_ha", "source", "state",
]

REQUIRED_POSITION_COLUMNS = ["latitude", "longitude"]
OPTIONAL_TELEMETRY_COLUMNS = [c for c in NORMALIZED_COLUMNS if c not in {"timestamp", "latitude", "longitude", "source", "state"}]
