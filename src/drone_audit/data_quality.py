from __future__ import annotations

import pandas as pd


def assess_data_quality(df: pd.DataFrame, source_type: str) -> list[str]:
    warnings: list[str] = []
    checks = {
        "has_spray_signal": any(c in df.columns and df[c].notna().any() for c in ["spray_on", "valve_open"]),
        "has_flow": "flow_l_min" in df.columns and pd.to_numeric(df["flow_l_min"], errors="coerce").notna().any(),
        "has_volume": "volume_total_l" in df.columns and pd.to_numeric(df["volume_total_l"], errors="coerce").notna().any(),
        "has_swath_width": "swath_width_m" in df.columns and pd.to_numeric(df["swath_width_m"], errors="coerce").notna().any(),
        "has_battery": "battery_pct" in df.columns and pd.to_numeric(df["battery_pct"], errors="coerce").notna().any(),
        "has_coordinates": {"latitude", "longitude"}.issubset(df.columns) and df[["latitude", "longitude"]].notna().any().all(),
        "has_timestamps": "timestamp" in df.columns and pd.to_datetime(df["timestamp"], errors="coerce", utc=True).notna().any(),
    }

    if not checks["has_spray_signal"]:
        warnings.append("sem_sinal_abertura_pulverizador")
    if not checks["has_flow"]:
        warnings.append("sem_vazao")
    if not checks["has_volume"]:
        warnings.append("sem_volume_aplicado")
    if not checks["has_swath_width"]:
        warnings.append("sem_largura_faixa")
    if not checks["has_battery"]:
        warnings.append("sem_bateria")
    if not checks["has_timestamps"]:
        warnings.extend(["sem_tempo", "sem_timestamps"])
    if not checks["has_coordinates"]:
        warnings.append("sem_coordenadas")
    if source_type.startswith("kml"):
        warnings.append("dados_kml_limitados")

    return warnings
