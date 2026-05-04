from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

SPRAYING_STATES = {"estimated_spraying", "pulverizando"}
MANEUVER_STATES = {"manobrando"}
TRANSIT_STATES = {"moving", "deslocando", "retorno_base"}
IDLE_STATES = {"idle", "parado", "troca_bateria", "reabastecimento"}


@dataclass(frozen=True)
class OperationalMetrics:
    tempo_total_s: float
    tempo_pulverizando_s: float
    tempo_manobrando_s: float
    tempo_deslocando_s: float
    tempo_parado_s: float
    eficiencia_operacional_pct: float | None
    produtividade_real_ha_h: float | None
    produtividade_pulverizando_ha_h: float | None
    consumo_bateria_ha_pct: float | None
    volume_por_ha_l: float | None
    taxa_real_l_ha: float | None


def _sum_states(durations: dict[str, float], accepted: set[str]) -> float:
    return float(sum(seconds for state, seconds in durations.items() if state in accepted))


def battery_usage_pct(df: pd.DataFrame) -> float | None:
    if "battery_pct" not in df.columns:
        return None
    values = pd.to_numeric(df["battery_pct"], errors="coerce").dropna()
    if len(values) < 2:
        return None
    return float(values.iloc[0] - values.iloc[-1])


def compute_operational_metrics(
    state_durations_s: dict[str, float],
    area_ha: float | None,
    tempo_total_s: float | None,
    battery_usage: float | None,
    volume_aplicado_l: float | None,
) -> OperationalMetrics:
    total = float(tempo_total_s or 0.0)
    pulverizando = _sum_states(state_durations_s, SPRAYING_STATES)
    manobrando = _sum_states(state_durations_s, MANEUVER_STATES)
    deslocando = _sum_states(state_durations_s, TRANSIT_STATES)
    parado = _sum_states(state_durations_s, IDLE_STATES)

    eficiencia = (pulverizando / total * 100.0) if total > 0 else None
    produtividade_real = (area_ha / (total / 3600.0)) if area_ha and total > 0 else None
    produtividade_pulv = (area_ha / (pulverizando / 3600.0)) if area_ha and pulverizando > 0 else None
    consumo_bat_ha = (battery_usage / area_ha) if battery_usage is not None and area_ha and area_ha > 0 else None
    volume_por_ha = (volume_aplicado_l / area_ha) if volume_aplicado_l is not None and area_ha and area_ha > 0 else None

    return OperationalMetrics(
        tempo_total_s=total,
        tempo_pulverizando_s=pulverizando,
        tempo_manobrando_s=manobrando,
        tempo_deslocando_s=deslocando,
        tempo_parado_s=parado,
        eficiencia_operacional_pct=eficiencia,
        produtividade_real_ha_h=produtividade_real,
        produtividade_pulverizando_ha_h=produtividade_pulv,
        consumo_bateria_ha_pct=consumo_bat_ha,
        volume_por_ha_l=volume_por_ha,
        taxa_real_l_ha=volume_por_ha,
    )


def generate_operational_alerts(metrics: OperationalMetrics) -> list[str]:
    alerts: list[str] = []
    if metrics.tempo_total_s > 0:
        manobra_pct = metrics.tempo_manobrando_s / metrics.tempo_total_s
        parado_pct = metrics.tempo_parado_s / metrics.tempo_total_s
        pulv_pct = metrics.tempo_pulverizando_s / metrics.tempo_total_s

        if manobra_pct > 0.25:
            alerts.append("Operação com excesso de tempo de manobra")
        if metrics.eficiencia_operacional_pct is not None and metrics.eficiencia_operacional_pct < 45:
            alerts.append("Baixa eficiência operacional")
        if pulv_pct < 0.4:
            alerts.append("Tempo pulverizando abaixo do ideal")
        if manobra_pct > 0.2 and pulv_pct < 0.5:
            alerts.append("Possível problema de planejamento de rota")
        if parado_pct > 0.2:
            alerts.append("Possível excesso de paradas para abastecimento ou troca de bateria")

    if metrics.consumo_bateria_ha_pct is not None and metrics.consumo_bateria_ha_pct > 8:
        alerts.append("Consumo de bateria acima do esperado")

    return alerts
