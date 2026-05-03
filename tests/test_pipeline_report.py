from drone_audit.pipeline import run_pipeline
from conftest import EXAMPLES


def test_pipeline_generates_report(tmp_path):
    output = tmp_path / "report.html"
    result = run_pipeline(csv_path=EXAMPLES / "sample_flight.csv", area_ha=12.5, output_path=output)
    assert output.exists()
    assert result.metrics["distance_m"] > 0
    assert "Drone Audit" in output.read_text(encoding="utf-8")
