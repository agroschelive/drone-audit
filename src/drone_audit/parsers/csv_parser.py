from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

import pandas as pd


@dataclass(frozen=True)
class ParsedCSV:
    dataframe: pd.DataFrame
    warnings: list[str]


def _normalize_column_name(name: str) -> str:
    name = name.strip().lower()
    name = re.sub(r"[^a-z0-9]+", "_", name)
    return name.strip("_")


def _find_first_column(columns: set[str], aliases: list[str]) -> str | None:
    for alias in aliases:
        normalized = _normalize_column_name(alias)
        if normalized in columns:
            return normalized
    return None


def _to_numeric(series: pd.Series | None) -> pd.Series:
    if series is None:
        return pd.Series(dtype="float64")
    return pd.to_numeric(series, errors="coerce")


def _normalize_boolean(value) -> bool | None:
    if pd.isna(value):
        return None
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    text = str(value).strip().lower()
    if text in {"1", "true", "yes", "y", "sim", "on", "open", "aberto", "spraying"}:
        return True
    if text in {"0", "false", "no", "n", "nao", "não", "off", "closed", "fechado", "idle"}:
        return False
    return None


def parse_csv(path: str | Path) -> ParsedCSV:
    csv_path = Path(path)
    warnings: list[str] = []
    df = pd.read_csv(csv_path, sep=None, engine="python")
    df = df.rename(columns={col: _normalize_column_name(str(col)) for col in df.columns})
    columns = set(df.columns)

    lat_col = _find_first_column(columns, ["latitude", "lat", "gps_lat", "latitude_deg"])
    lon_col = _find_first_column(columns, ["longitude", "lon", "lng", "gps_lon", "longitude_deg"])
    ts_col = _find_first_column(columns, ["timestamp", "time", "datetime", "record_time", "date_time"])
    alt_col = _find_first_column(columns, ["altitude_m", "altitude", "height", "rel_alt", "relative_altitude"])
    speed_ms_col = _find_first_column(columns, ["speed_m_s", "ground_speed_m_s", "velocity_m_s"])
    speed_kmh_col = _find_first_column(columns, ["speed_km_h", "speed_kmh", "ground_speed_kmh"])
    valve_col = _find_first_column(columns, ["valve_open", "spray_on", "spraying", "pump_on", "material_on"])
    battery_col = _find_first_column(columns, ["battery_pct", "battery_percent", "battery", "soc", "battery_level"])

    if lat_col is None or lon_col is None:
        warnings.append("CSV does not contain recognizable latitude/longitude columns.")

    out = pd.DataFrame(index=df.index)
    out["timestamp"] = pd.to_datetime(df[ts_col], errors="coerce", utc=True) if ts_col else pd.NaT
    out["latitude"] = _to_numeric(df[lat_col]) if lat_col else pd.NA
    out["longitude"] = _to_numeric(df[lon_col]) if lon_col else pd.NA
    out["altitude_m"] = _to_numeric(df[alt_col]) if alt_col else pd.NA

    if speed_ms_col:
        out["speed_m_s"] = _to_numeric(df[speed_ms_col])
    elif speed_kmh_col:
        out["speed_m_s"] = _to_numeric(df[speed_kmh_col]) / 3.6
    else:
        out["speed_m_s"] = pd.NA
        warnings.append("CSV does not contain a recognizable speed column.")

    out["valve_open"] = df[valve_col].apply(_normalize_boolean) if valve_col else None
    out["battery_pct"] = _to_numeric(df[battery_col]) if battery_col else pd.NA
    out["source"] = "csv"

    return ParsedCSV(dataframe=out, warnings=warnings)
