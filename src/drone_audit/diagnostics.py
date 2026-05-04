from __future__ import annotations


def diagnose_operational(metrics: dict, data_quality_warnings: list[str] | None = None, spray_anomalies: list[dict] | None = None, planned_rate_l_ha: float | None = None) -> list[dict]:
    op = metrics.get("operational", {})
    dq = data_quality_warnings or []
    anomalies = {a.get("code") for a in (spray_anomalies or [])}
    alerts: list[dict] = []
    total = op.get("tempo_total_s") or (op.get("spray_time_s", 0) + op.get("non_spray_moving_time_s", 0) + op.get("idle_time_s", 0)) or 0
    eff = op.get("eficiencia_operacional_pct") or 0
    moving = op.get("tempo_manobrando_s") or op.get("non_spray_moving_time_s") or 0
    idle = op.get("tempo_parado_s") or op.get("idle_time_s") or 0
    if eff < 50:
        alerts.append({"code": "baixa_eficiencia_operacional", "severity": "warning", "message": "Eficiência operacional baixa.", "evidence": {"eficiencia_operacional_pct": eff}})
    if total and moving / total > 0.25:
        alerts.append({"code": "excesso_manobra", "severity": "warning", "message": "Tempo alto em deslocamento sem pulverizar.", "evidence": {"percentual": moving / total * 100}})
    if total and idle / total > 0.15:
        alerts.append({"code": "excesso_parado", "severity": "warning", "message": "Tempo parado acima do esperado.", "evidence": {"percentual": idle / total * 100}})
    if "deslocando_sem_pulverizar" in anomalies or (total and moving / total > 0.25):
        alerts.append({"code": "deslocamento_sem_pulverizar", "severity": "warning", "message": "Há deslocamento sem pulverização relevante.", "evidence": {"anomalias": list(anomalies)}})
    if "spray_ligado_parado" in anomalies:
        alerts.append({"code": "spray_ligado_parado", "severity": "critical", "message": "Pulverizador ligado com baixa velocidade.", "evidence": {}})
    if "sem_largura_faixa" in dq or "pulverizacao_sem_largura_faixa" in anomalies:
        alerts.append({"code": "falta_dado_faixa", "severity": "warning", "message": "Faltam dados de largura de faixa.", "evidence": {}})
    if "sem_volume_aplicado" in dq:
        alerts.append({"code": "falta_dado_volume", "severity": "warning", "message": "Faltam dados de volume aplicado.", "evidence": {}})
    if "sem_sinal_abertura_pulverizador" in dq:
        alerts.append({"code": "falta_dado_spray", "severity": "warning", "message": "Faltam sinais de acionamento do pulverizador.", "evidence": {}})
    bpha = metrics.get("battery_per_ha_pct")
    if bpha is not None and bpha > 20:
        alerts.append({"code": "alto_consumo_bateria_por_ha", "severity": "warning", "message": "Consumo de bateria por hectare elevado.", "evidence": {"battery_per_ha_pct": bpha}})
    taxa = op.get("taxa_real_l_ha") or metrics.get("real_rate_l_ha")
    if planned_rate_l_ha and taxa is not None and abs(taxa - planned_rate_l_ha) / planned_rate_l_ha > 0.2:
        alerts.append({"code": "taxa_real_fora_do_planejado", "severity": "warning", "message": "Taxa real divergente do planejado.", "evidence": {"taxa_real_l_ha": taxa, "planejada": planned_rate_l_ha}})
    if sum(x in dq for x in ["sem_volume_aplicado", "sem_largura_faixa", "sem_sinal_abertura_pulverizador", "sem_tempo"]) >= 2:
        alerts.append({"code": "pouca_telemetria", "severity": "critical", "message": "Telemetria insuficiente para auditoria robusta.", "evidence": {"warnings": dq}})
    if eff >= 70 and not any(a["severity"] in {"warning", "critical"} for a in alerts):
        alerts.append({"code": "operacao_eficiente", "severity": "info", "message": "Operação eficiente para os dados disponíveis.", "evidence": {"eficiencia_operacional_pct": eff}})
    return alerts
