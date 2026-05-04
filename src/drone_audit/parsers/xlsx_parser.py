from __future__ import annotations

import re
import unicodedata
from pathlib import Path

import pandas as pd

from drone_audit.parsers.base import ParsedData


def _norm(name: str) -> str:
    raw = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", "_", raw.strip().lower()).strip("_")


ALIASES = {
    "data_hora_inicio": "timestamp_start",
    "start_time": "timestamp_start",
    "inicio": "timestamp_start",
    "data_hora_fim": "timestamp_end",
    "end_time": "timestamp_end",
    "fim": "timestamp_end",
    "data_hora": "timestamp",
    "timestamp": "timestamp",
    "duracao_s": "duration_s",
    "duration_s": "duration_s",
    "duracao": "duration_s",
    "drone_model": "drone_model",
    "modelo_drone": "drone_model",
    "drone_serial": "drone_serial",
    "serial_drone": "drone_serial",
    "battery_serial": "battery_serial",
    "serial_bateria": "battery_serial",
    "operator": "operator",
    "operador": "operator",
    "farm_name": "farm_name",
    "fazenda": "farm_name",
    "field_name": "field_name",
    "talhao": "field_name",
    "area_ha": "area_ha",
    "area": "area_ha",
    "distance_m": "distance_m",
    "distancia_m": "distance_m",
    "volume_l": "volume_l",
    "volume": "volume_l",
    "application_rate_l_ha": "application_rate_l_ha",
    "taxa_l_ha": "application_rate_l_ha",
    "speed_m_s": "speed_m_s",
    "velocidade_m_s": "speed_m_s",
    "altitude_m": "altitude_m",
    "altura_m": "altitude_m",
    "battery_start_pct": "battery_start_pct",
    "bateria_inicio_pct": "battery_start_pct",
    "battery_end_pct": "battery_end_pct",
    "bateria_fim_pct": "battery_end_pct",
    "battery_consumed_pct": "battery_consumed_pct",
    "bateria_consumida_pct": "battery_consumed_pct",
}

NORMALIZED_COLUMNS = [
    "timestamp_start","timestamp_end","timestamp","duration_s","drone_model","drone_serial",
    "battery_serial","operator","farm_name","field_name","area_ha","distance_m","volume_l",
    "application_rate_l_ha","speed_m_s","altitude_m","battery_start_pct","battery_end_pct","battery_consumed_pct",
]


def parse_xlsx(path: str | Path, sheet: int | str = 0) -> ParsedData:
    warnings: list[str] = []
    df = pd.read_excel(path, sheet_name=sheet, engine="openpyxl")
    renamed = {c: ALIASES.get(_norm(str(c)), _norm(str(c))) for c in df.columns}
    df = df.rename(columns=renamed)
    out = pd.DataFrame(index=df.index)
    for col in NORMALIZED_COLUMNS:
        out[col] = df[col] if col in df.columns else pd.NA

    for col in ["timestamp_start", "timestamp_end", "timestamp"]:
        out[col] = pd.to_datetime(out[col], errors="coerce", utc=True)
    for col in ["duration_s", "area_ha", "distance_m", "volume_l", "application_rate_l_ha", "speed_m_s", "altitude_m", "battery_start_pct", "battery_end_pct", "battery_consumed_pct"]:
        out[col] = pd.to_numeric(out[col], errors="coerce")

    if out["timestamp"].isna().all() and out["timestamp_start"].notna().any():
        out["timestamp"] = out["timestamp_start"]
    if out["duration_s"].isna().all() and out["timestamp_start"].notna().any() and out["timestamp_end"].notna().any():
        out["duration_s"] = (out["timestamp_end"] - out["timestamp_start"]).dt.total_seconds()

    missing = [c for c in NORMALIZED_COLUMNS if out[c].isna().all()]
    if missing:
        warnings.append(f"xlsx_campos_ausentes: {', '.join(missing)}")

    return ParsedData(dataframe=out, warnings=warnings, source_type="xlsx_smartfarm")
