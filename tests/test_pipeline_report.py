from drone_audit.pipeline import run_pipeline
from conftest import EXAMPLES


def test_pipeline_generates_report(tmp_path):
    output = tmp_path / "report.html"
    result = run_pipeline(csv_path=EXAMPLES / "sample_flight.csv", area_ha=12.5, output_path=output)
    assert output.exists()
    assert result.metrics["distance_m"] > 0
    assert "Drone Audit" in output.read_text(encoding="utf-8")


def test_pipeline_handles_corrupted_rows_and_invalid_coordinates(tmp_path):
    csv_path = tmp_path / "bad_input.csv"
    csv_path.write_text(
        "\n".join(
            [
                "timestamp,latitude,longitude,speed_m_s,valve_open",
                "2026-01-01T00:00:00Z,-23.0,-46.0,2.0,true",
                "not-a-date,-23.01,-46.01,2.0,true",
                "2026-01-01T00:00:20Z,200,-46.02,2.0,false",
                "oops,too,many,columns,ignored,here",
                "2026-01-01T00:00:40Z,-23.02,-46.03,2.0,false",
            ]
        ),
        encoding="utf-8",
    )

    result = run_pipeline(csv_path=csv_path)
    assert result.metrics["distance_m"] > 0
    assert result.metrics["time_s"] == 40.0
    assert any("invalid timestamps" in msg for msg in result.warnings)
    assert any("out-of-range coordinates" in msg for msg in result.warnings)
