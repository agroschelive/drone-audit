from drone_audit.agras.types.agras_models import AgrasFlight, AgrasTelemetryPoint

MOCK_VOOS=[
    AgrasFlight(modelo_agras='T40', area_aplicada_ha=8.2, volume_aplicado_l=98, bateria_inicial_pct=96, bateria_final_pct=24),
    AgrasFlight(modelo_agras='T40', area_aplicada_ha=7.9, volume_aplicado_l=93, bateria_inicial_pct=97, bateria_final_pct=18),
    AgrasFlight(modelo_agras='T40', area_aplicada_ha=8.5, volume_aplicado_l=102, bateria_inicial_pct=95, bateria_final_pct=22),
]
MOCK_PONTOS=[AgrasTelemetryPoint(latitude=-15.0, longitude=-47.0, sequencia=1, velocidade_ms=4.2, spray_ligado=True, area_acumulada_ha=0.1)]
