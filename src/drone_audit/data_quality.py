from __future__ import annotations

import pandas as pd


def has_coordinates(df: pd.DataFrame) -> bool:
    return {"latitude", "longitude"}.issubset(df.columns) and df[["latitude", "longitude"]].notna().any().all()


def has_timestamps(df: pd.DataFrame) -> bool:
    return "timestamp" in df.columns and pd.to_datetime(df["timestamp"], errors="coerce", utc=True).notna().any()


def has_spray_signal(df: pd.DataFrame) -> bool:
    return ("valve_open" in df.columns and df["valve_open"].notna().any()) or (
        "volume_l" in df.columns and pd.to_numeric(df["volume_l"], errors="coerce").fillna(0).sum() > 0
    )


def has_battery_data(df: pd.DataFrame) -> bool:
    cols = [c for c in ["battery_pct", "battery_start_pct", "battery_end_pct", "battery_consumed_pct"] if c in df.columns]
    return any(df[c].notna().any() for c in cols)


def has_flow_or_volume(df: pd.DataFrame) -> bool:
    return ("volume_l" in df.columns and pd.to_numeric(df["volume_l"], errors="coerce").fillna(0).sum() > 0) or (
        "application_rate_l_ha" in df.columns and pd.to_numeric(df["application_rate_l_ha"], errors="coerce").notna().any()
    )


def has_area_data(df: pd.DataFrame) -> bool:
    return "area_ha" in df.columns and pd.to_numeric(df["area_ha"], errors="coerce").notna().any()


def assess_data_quality(df: pd.DataFrame, source_type: str) -> list[str]:
    warnings: list[str] = []
    if not has_timestamps(df):
        warnings.append("sem_timestamps")
    if not has_battery_data(df):
        warnings.append("sem_bateria")
    if not has_spray_signal(df):
        warnings.append("sem_sinal_pulverizacao")
    if not has_flow_or_volume(df):
        warnings.append("sem_vazao_volume")
    if source_type.startswith("kml") and not has_flow_or_volume(df):
        warnings.append("kml_com_telemetria_limitada")
    if len(warnings) >= 3:
        warnings.append("dados_insuficientes_para_estado_operacional")
    return warnings
