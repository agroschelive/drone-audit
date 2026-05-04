from __future__ import annotations
from drone_audit.agras.types.agras_models import AgrasDiagnostic, AgrasFlightMetrics

def generate_agras_diagnostics(metrics: AgrasFlightMetrics, has_telemetry: bool) -> list[AgrasDiagnostic]:
    out=[]
    if not has_telemetry:
        out.append(AgrasDiagnostic(codigo='pouca_informacao_telemetria', mensagem='O arquivo importado possui poucos dados de telemetria. Algumas métricas foram estimadas.', severidade='warning'))
    eff = metrics.eficiencia_operacional_pct
    if eff is not None and eff < 40:
        out.append(AgrasDiagnostic(codigo='baixa_eficiencia_operacional', mensagem='A operação teve baixa eficiência operacional. O drone passou pouco tempo pulverizando em relação ao tempo total de voo.', severidade='warning'))
    if eff is not None and eff >= 70:
        out.append(AgrasDiagnostic(codigo='operacao_eficiente', mensagem='Boa eficiência operacional. A maior parte do tempo de voo foi usada em aplicação efetiva.', severidade='info'))
    return out
