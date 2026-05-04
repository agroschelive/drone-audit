from drone_audit.diagnostics import diagnose_operational

def _codes(alerts): return {a['code'] for a in alerts}

def test_alerts_core():
    metrics={"operational":{"eficiencia_operacional_pct":40,"tempo_total_s":100,"tempo_manobrando_s":30,"tempo_parado_s":20,"taxa_real_l_ha":30},"battery_per_ha_pct":25}
    alerts=diagnose_operational(metrics,["sem_largura_faixa","sem_volume_aplicado"],[{"code":"spray_ligado_parado"},{"code":"deslocando_sem_pulverizar"}],20)
    c=_codes(alerts)
    assert "baixa_eficiencia_operacional" in c and "spray_ligado_parado" in c and "falta_dado_faixa" in c and "taxa_real_fora_do_planejado" in c

def test_operacao_eficiente():
    metrics={"operational":{"eficiencia_operacional_pct":80,"tempo_total_s":100,"tempo_manobrando_s":5,"tempo_parado_s":5}}
    alerts=diagnose_operational(metrics,[],[],20)
    assert _codes(alerts)=={"operacao_eficiente"}
