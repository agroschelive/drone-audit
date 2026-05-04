from __future__ import annotations

import re

ALIASES = {
    "timestamp": ["timestamp", "time", "datetime", "date_time", "data_hora", "hora", "utc_time"],
    "latitude": ["latitude", "lat", "gps_lat", "aircraft_latitude"],
    "longitude": ["longitude", "lon", "lng", "gps_lon", "aircraft_longitude"],
    "altitude_m": ["altitude", "height", "altitude_m", "height_m", "relative_altitude"],
    "speed_m_s": ["speed", "velocity", "speed_m_s", "ground_speed", "horizontal_speed"],
    "battery_pct": ["battery", "battery_pct", "battery_percent", "remaining_battery", "battery_level"],
    "spray_on": ["spray_on", "spraying", "is_spraying", "sprayer_on", "spray_state", "spray_status"],
    "valve_open": ["valve_open", "valve", "valve_state", "nozzle_open", "spray_valve"],
    "pump_on": ["pump_on", "pump", "pump_state"],
    "flow_l_min": ["flow", "flow_rate", "flow_l_min", "liquid_flow", "spray_flow", "application_flow"],
    "volume_total_l": ["volume", "total_volume", "volume_l", "spray_volume", "total_spray_volume", "liquid_volume", "pesticide_volume"],
    "swath_width_m": ["swath", "swath_width", "width", "spray_width", "application_width", "faixa", "largura_faixa"],
    "area_total_ha": ["area", "area_ha", "applied_area", "spray_area", "worked_area", "hectares"],
}


def normalize_column_name(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", str(name).strip().lower()).strip("_")


def map_columns(columns: list[str]) -> dict[str, str]:
    normalized = {normalize_column_name(c): c for c in columns}
    mapping: dict[str, str] = {}
    for target, aliases in ALIASES.items():
        for alias in aliases:
            if normalize_column_name(alias) in normalized:
                mapping[target] = normalized[normalize_column_name(alias)]
                break
    return mapping
