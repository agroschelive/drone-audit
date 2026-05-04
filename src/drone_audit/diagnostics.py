from __future__ import annotations


def diagnose_operational(metrics: dict, data_quality_warnings: list[str] | None = None) -> list[dict]:
    op = metrics.get("operational", {})
    alerts: list[dict] = []

    eff = op.get("eficiencia_operacional_pct") or 0
    if eff < 50:
        alerts.append(
            {
                "code": "baixa_eficiencia_operacional",
                "severity": "warning",
                "message": "Eficiência operacional baixa.",
                "evidence": {"eficiencia": eff},
            }
        )

    taxa = op.get("taxa_real_l_ha")
    if taxa is not None and (taxa < 5 or taxa > 40):
        alerts.append(
            {
                "code": "taxa_real_fora_do_planejado",
                "severity": "warning",
                "message": "Taxa real fora do planejado.",
                "evidence": {"taxa_real_l_ha": taxa},
            }
        )

    if not alerts:
        alerts.append(
            {
                "code": "operacao_eficiente",
                "severity": "info",
                "message": "Operação eficiente para os dados disponíveis.",
                "evidence": {"eficiencia": eff},
            }
        )

    return alerts
