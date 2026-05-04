from drone_audit.agras.analyzers.calculate_agras_metrics import calculate_agras_metrics
from drone_audit.agras.analyzers.classify_agras_events import classify_agras_events
from drone_audit.agras.analyzers.generate_agras_diagnostics import generate_agras_diagnostics
from drone_audit.agras.parsers.smartfarm_kml_parser import parse_smartfarm_kml
from drone_audit.agras.utils.agras_units import area_to_ha
from drone_audit.agras.types.agras_models import AgrasFlight, AgrasTelemetryPoint


def test_area_conversion():
    assert round(area_to_ha(10, 'acres'), 4) == 4.0469

def test_kml_parser_reads_points():
    pts = parse_smartfarm_kml('examples/sample_track_gx.kml')
    assert len(pts) > 0

def test_event_classification_basic():
    voo=AgrasFlight()
    ev=classify_agras_events(voo,[AgrasTelemetryPoint(latitude=0, longitude=0, sequencia=1, velocidade_ms=4, spray_ligado=False)])
    assert ev[0].tipo_evento == 'deslocando_sem_pulverizar'

def test_efficiency_metric_and_diag():
    voo=AgrasFlight(area_aplicada_ha=5)
    ev=classify_agras_events(voo,[AgrasTelemetryPoint(latitude=0, longitude=0, sequencia=1, spray_ligado=True)])
    m=calculate_agras_metrics(voo,ev,3600)
    assert m.eficiencia_operacional_pct == 100
    d=generate_agras_diagnostics(m, has_telemetry=True)
    assert any(x.codigo=='operacao_eficiente' for x in d)
