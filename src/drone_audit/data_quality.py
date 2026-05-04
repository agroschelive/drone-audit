from __future__ import annotations

import pandas as pd


def assess_data_quality(df: pd.DataFrame, source_type: str) -> list[str]:
    categories = {
        "dados_ausentes": [],
        "baixa_confianca": [],
        "formato_nao_suportado": [],
        "diagnostico_operacional": [],
    }
    if df.empty:
        categories["dados_ausentes"].append("fonte_sem_telemetria_ponto_a_ponto")
    if (
        "timestamp" not in df.columns
        or pd.to_datetime(df.get("timestamp"), errors="coerce", utc=True).isna().all()
    ):
        categories["baixa_confianca"].extend(
            ["sem_tempo", "sem_timestamps", "tempo_estimado_por_linhas"]
        )
    if {"latitude", "longitude"}.issubset(df.columns) and df[
        ["latitude", "longitude"]
    ].isna().all().all():
        categories["dados_ausentes"].append("sem_coordenadas")

    if "battery_pct" not in df.columns or pd.to_numeric(df.get("battery_pct"), errors="coerce").isna().all():
        categories["dados_ausentes"].append("sem_bateria")

    if source_type == "dat":
        categories["formato_nao_suportado"].append("formato_dat_nao_suportado")
    if "timestamp" in df.columns:
        ts = pd.to_datetime(df.get("timestamp"), errors="coerce", utc=True)
        if ts.notna().any() and not ts.dropna().is_monotonic_increasing:
            categories["diagnostico_operacional"].append("timestamps_fora_de_ordem")
    out: list[str] = []
    for vals in categories.values():
        out.extend(vals)
    return out
