from __future__ import annotations

import pandas as pd

from drone_audit.field_aliases import map_columns


def _to_num(series: pd.Series | None) -> pd.Series:
    if series is None:
        return pd.Series(dtype="float64")
    s = series.astype("string").str.replace(",", ".", regex=False)
    return pd.to_numeric(s, errors="coerce")


def normalize_telemetry_dataframe(df, source_type: str) -> tuple[pd.DataFrame, list[str]]:
    warnings: list[str] = []
    out = pd.DataFrame(index=df.index)
    mapping = map_columns([str(c) for c in df.columns])
    for col in ["timestamp","latitude","longitude","altitude_m","speed_m_s","heading_deg","battery_pct","voltage_v","current_a","spray_on","valve_open","pump_on","flow_l_min","volume_total_l","swath_width_m","area_total_ha"]:
        src = mapping.get(col)
        out[col] = df[src] if src else pd.NA

    out["timestamp"] = pd.to_datetime(out["timestamp"], errors="coerce", utc=True)
    for n in ["latitude","longitude","altitude_m","speed_m_s","heading_deg","battery_pct","voltage_v","current_a","flow_l_min","volume_total_l","swath_width_m","area_total_ha"]:
        out[n] = _to_num(out[n])

    cols_norm = {str(c).lower(): c for c in df.columns}
    if any("km/h" in c.lower() or "kmh" in c.lower() for c in df.columns):
        out["speed_m_s"] = out["speed_m_s"] / 3.6
    if any("m2" in c.lower() or "m²" in c.lower() for c in df.columns):
        out["area_total_ha"] = out["area_total_ha"] / 10000.0
    if any("ml" in c.lower() for c in df.columns):
        out["volume_total_l"] = out["volume_total_l"] / 1000.0

    out["source"] = source_type
    if out["timestamp"].isna().all(): warnings.append("sem_tempo")
    if out[["latitude", "longitude"]].isna().all().all(): warnings.append("sem_coordenadas")
    return out, warnings
