from __future__ import annotations


def diagnose_operational(metrics: dict, data_quality_warnings: list[str] | None = None) -> list[dict]:
    data_quality_warnings = data_quality_warnings or []
    op = metrics.get("operational", {})
    alerts = []
    if "dados_insuficientes_para_estado_operacional" in data_quality_warnings:
        return [{"code": "dados_insuficientes", "severity": "alta", "message": "Dados insuficientes para diagnóstico robusto.", "evidence": data_quality_warnings}]

    eff = op.get("eficiencia_operacional_pct") or 0
    man = op.get("tempo_manobrando_s") or 0
    par = op.get("tempo_parado_s") or 0
    total = max(op.get("tempo_total_s") or 0, 1)
    bat = op.get("consumo_bateria_ha_pct") or 0
    prod = op.get("produtividade_real_ha_h") or 0
    taxa = op.get("taxa_real_l_ha")

    if eff < 50:
        alerts.append({"code": "baixa_eficiencia_operacional", "severity": "media", "message": "Eficiência operacional baixa.", "evidence": {"eficiencia_operacional_pct": eff}})
    if man / total > 0.35:
        alerts.append({"code": "excesso_manobra", "severity": "media", "message": "Tempo de manobra elevado.", "evidence": {"tempo_manobrando_s": man, "tempo_total_s": total}})
    if par / total > 0.25:
        alerts.append({"code": "excesso_parado", "severity": "media", "message": "Tempo parado elevado.", "evidence": {"tempo_parado_s": par, "tempo_total_s": total}})
    if bat > 15:
        alerts.append({"code": "alto_consumo_bateria_por_ha", "severity": "media", "message": "Consumo de bateria por hectare acima do esperado.", "evidence": {"consumo_bateria_ha_pct": bat}})
    if prod < 3:
        alerts.append({"code": "baixa_produtividade", "severity": "baixa", "message": "Produtividade baixa para o perfil da operação.", "evidence": {"produtividade_real_ha_h": prod}})
    if "kml_com_telemetria_limitada" in data_quality_warnings:
        alerts.append({"code": "pouca_telemetria", "severity": "baixa", "message": "Telemetria limitada para inferências avançadas.", "evidence": data_quality_warnings})
    if man / total > 0.45 and eff < 55:
        alerts.append({"code": "possivel_rota_mal_planejada", "severity": "media", "message": "Possível rota mal planejada.", "evidence": {"manobra_ratio": man / total, "eficiencia": eff}})
    if taxa is not None and (taxa < 5 or taxa > 40):
        alerts.append({"code": "taxa_real_fora_do_planejado", "severity": "media", "message": "Taxa real fora da faixa esperada.", "evidence": {"taxa_real_l_ha": taxa}})
    if not alerts:
        alerts.append({"code": "operacao_eficiente", "severity": "info", "message": "Operação com indicadores dentro do esperado.", "evidence": {"eficiencia_operacional_pct": eff}})
    return alerts
