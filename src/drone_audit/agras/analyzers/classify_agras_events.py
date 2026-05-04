from __future__ import annotations
from drone_audit.agras.types.agras_models import AgrasFlight, AgrasOperationalEvent, AgrasTelemetryPoint

def classify_agras_events(voo: AgrasFlight, pontos: list[AgrasTelemetryPoint]) -> list[AgrasOperationalEvent]:
    if not pontos:
        return [AgrasOperationalEvent(tipo_evento='desconhecido', inicio=voo.inicio, fim=voo.fim, confianca=0.2, observacao='Sem telemetria detalhada; evento estimado.')]
    spraying = any((p.spray_ligado is True) or ((p.volume_acumulado_l or 0) > 0) or ((p.area_acumulada_ha or 0) > 0) for p in pontos)
    if spraying:
        return [AgrasOperationalEvent(tipo_evento='pulverizando', inicio=voo.inicio, fim=voo.fim, confianca=0.7)]
    moving = any((p.velocidade_ms or 0) > 0.5 for p in pontos)
    return [AgrasOperationalEvent(tipo_evento='deslocando_sem_pulverizar' if moving else 'parado', inicio=voo.inicio, fim=voo.fim, confianca=0.6)]
