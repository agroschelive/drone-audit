from drone_audit.diagnostics import diagnose_operational


def test_diagnostics_low_efficiency():
    alerts = diagnose_operational({'operational': {'eficiencia_operacional_pct': 40, 'tempo_manobrando_s': 400, 'tempo_total_s': 800, 'tempo_parado_s': 300, 'consumo_bateria_ha_pct': 20, 'produtividade_real_ha_h': 2, 'taxa_real_l_ha': 50}},[])
    codes = {a['code'] for a in alerts}
    assert 'baixa_eficiencia_operacional' in codes
    assert 'taxa_real_fora_do_planejado' in codes
