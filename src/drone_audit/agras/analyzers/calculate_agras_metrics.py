from __future__ import annotations
from drone_audit.agras.types.agras_models import AgrasFlight, AgrasFlightMetrics, AgrasOperationalEvent

def calculate_agras_metrics(voo: AgrasFlight, eventos: list[AgrasOperationalEvent], tempo_total_s: float | None) -> AgrasFlightMetrics:
    t = tempo_total_s
    spray = t if any(e.tipo_evento=='pulverizando' for e in eventos) and t else 0
    desloc = t if any(e.tipo_evento=='deslocando_sem_pulverizar' for e in eventos) and t else 0
    parado = t if any(e.tipo_evento=='parado' for e in eventos) and t else 0
    eficiencia = (spray / t * 100.0) if t and t>0 else None
    prod = (voo.area_aplicada_ha / (t/3600.0)) if (t and t>0 and voo.area_aplicada_ha) else None
    return AgrasFlightMetrics(tempo_total_segundos=t, tempo_pulverizando_segundos=spray, tempo_deslocando_segundos=desloc, tempo_parado_segundos=parado, eficiencia_operacional_pct=eficiencia, produtividade_real_ha_h=prod)
