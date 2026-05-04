from drone_audit.pipeline import run_pipeline
from conftest import EXAMPLES


def test_pipeline_generates_report(tmp_path):
    output = tmp_path / "report.html"
    result = run_pipeline(csv_path=EXAMPLES / "sample_flight.csv", area_ha=12.5, output_path=output)
    assert output.exists()
    assert result.metrics["distance_m"] > 0
    html = output.read_text(encoding="utf-8")
    assert "Drone Audit - Relatório Auxiliar" in html
    assert "Avisos técnicos" in html


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

    output = tmp_path / "bad_report.html"
    result = run_pipeline(csv_path=csv_path, output_path=output)
    assert result.metrics["distance_m"] > 0
    assert result.metrics["time_s"] == 40.0
    assert any("invalid timestamps" in msg for msg in result.warnings)
    assert any("out-of-range coordinates" in msg for msg in result.warnings)


def test_corrupted_csv_warnings_are_rendered_in_html_report(tmp_path):
    csv_path = tmp_path / "bad_input_for_report.csv"
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

    output = tmp_path / "corrupted_report.html"
    run_pipeline(csv_path=csv_path, output_path=output)

    html = output.read_text(encoding="utf-8")
    assert "Avisos técnicos" in html
    assert "CSV contains" in html
    assert "dataset may be incomplete" in html
    assert "invalid timestamps" in html
    assert "out-of-range coordinates" in html


def test_pipeline_uses_swath_width_and_effective_area_in_metrics(tmp_path):
    csv_path = tmp_path / "swath.csv"
    csv_path.write_text("\n".join([
        "timestamp,latitude,longitude,speed_m_s,valve_open",
        "2026-01-01T00:00:00Z,-23.0,-46.0,2.0,true",
        "2026-01-01T00:00:10Z,-23.0,-45.999,2.0,true",
    ]), encoding="utf-8")

    result = run_pipeline(csv_path=csv_path, swath_width_m=10.0, output_path=tmp_path / "report.html")
    assert "swath_width_m" in result.dataframe.columns
    assert result.metrics["applied_area_ha"] is not None
    assert result.metrics["effective_area_ha"] == result.metrics["applied_area_ha"]


def test_report_shows_all_area_variants(tmp_path):
    output = tmp_path / "report_areas.html"
    run_pipeline(csv_path=EXAMPLES / "sample_flight.csv", area_ha=12.5, output_path=output)
    html = output.read_text(encoding="utf-8")
    assert "Área informada" in html
    assert "Área calculada" in html
    assert "Área usada nos cálculos" in html


def test_pipeline_csv_plus_dat_keeps_csv_source(tmp_path):
    csv_path = tmp_path / "s.csv"
    csv_path.write_text("timestamp,latitude,longitude\n2026-01-01T00:00:00Z,-23,-46\n2026-01-01T00:00:10Z,-23,-45.999", encoding="utf-8")
    dat_path = tmp_path / "a.dat"
    dat_path.write_bytes(b"fake")
    result = run_pipeline(csv_path=csv_path, dat_path=dat_path)
    assert result.metrics["data_source"] == "csv"

def test_report_sections_rendered(tmp_path):
    output = tmp_path / "r.html"
    run_pipeline(csv_path=EXAMPLES / "sample_flight.csv", output_path=output)
    html = output.read_text(encoding="utf-8")
    assert "Confiabilidade dos dados" in html
    assert "Limitações da análise" in html
    assert "Avisos técnicos" in html
