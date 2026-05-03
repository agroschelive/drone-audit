from drone_audit.classifier import classify_states
from drone_audit.metrics import productivity_ha_h, total_distance_m, total_time_s
from drone_audit.parsers.csv_parser import parse_csv
from conftest import EXAMPLES


def test_metrics_and_classifier():
    df = parse_csv(EXAMPLES / "sample_flight.csv").dataframe
    classified = classify_states(df)
    assert total_distance_m(classified) > 0
    assert total_time_s(classified) == 40.0
    assert productivity_ha_h(10, 3600) == 10
    assert "pulverizando_estimado" in classified["state"].tolist()
