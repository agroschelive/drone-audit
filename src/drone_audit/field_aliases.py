from __future__ import annotations

import re

ALIASES = {
    "timestamp": ["timestamp", "time", "datetime", "date_time", "data_hora", "hora", "utc_time"],
    "latitude": ["latitude", "lat", "gps_lat", "aircraft_latitude"],
    "longitude": ["longitude", "lon", "lng", "gps_lon", "aircraft_longitude"],
    "altitude_m": ["altitude", "height", "altitude_m", "height_m", "relative_altitude"],
    "speed_m_s": ["speed", "velocity", "speed_m_s", "ground_speed", "horizontal_speed", "speed_km_h", "velocidade", "velocidade_km_h"],
    "heading_deg": ["heading", "yaw", "heading_deg", "rumo"],
    "battery_pct": ["battery", "battery_pct", "battery_percent", "remaining_battery", "bateria", "bateria_pct", "bateria_percentual"],
    "voltage_v": ["voltage", "voltage_v", "tensao", "tensão", "bateria_v"],
    "current_a": ["current", "current_a", "corrente", "amperagem"],
    "spray_on": ["spray_on", "spray", "sprayer", "spraying", "spray_status", "spray_state", "pulverizacao", "pulverizando", "pulverizador", "pulverizador_ligado"],
    "valve_open": ["valve", "valve_open", "spray_valve", "nozzle", "nozzle_open", "valvula", "válvula", "valvula_aberta", "bico_aberto"],
    "pump_on": ["pump", "pump_on", "bomba", "bomba_ligada"],
    "flow_l_min": ["flow", "flow_rate", "flow_l_min", "liquid_flow", "spray_flow", "vazao", "vazão", "vazao_l_min", "fluxo", "fluxo_l_min"],
    "volume_total_l": ["volume", "volume_l", "volume_ml", "total_volume", "total_spray_volume", "spray_volume", "liquid_volume", "volume_aplicado", "volume_total", "calda_l", "calda_aplicada"],
    "swath_width_m": ["swath", "swath_width", "spray_width", "application_width", "largura_faixa", "faixa", "largura", "largura_aplicacao"],
    "area_total_ha": ["area", "área", "area_ha", "area_total_ha", "area_m2", "area_m", "spray_area", "applied_area", "worked_area", "area_aplicada", "area_total", "hectares", "ha", "area_aplicada"],
}


def normalize_column_name(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", str(name).strip().lower()).strip("_")


def map_columns(columns: list[str]) -> dict[str, str]:
    normalized = {normalize_column_name(c): c for c in columns}
    mapping: dict[str, str] = {}
    for target, aliases in ALIASES.items():
        for alias in aliases:
            key = normalize_column_name(alias)
            if key in normalized:
                mapping[target] = normalized[key]
                break
    return mapping
