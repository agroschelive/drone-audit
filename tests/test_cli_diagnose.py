import json

from drone_audit.cli import main
from conftest import EXAMPLES


def test_cli_diagnose_includes_diagnostics(tmp_path, capsys):
    output = tmp_path / "report.html"

    rc = main(
        [
            "--csv",
            str(EXAMPLES / "sample_flight.csv"),
            "--area-ha",
            "12.5",
            "--output",
            str(output),
            "--diagnose",
        ]
    )

    assert rc == 0
    payload = json.loads(capsys.readouterr().out)
    assert "diagnostics" in payload

    diagnostics = payload["diagnostics"]
    assert set(
        [
            "rows",
            "columns",
            "recognized_inputs",
            "valid_coordinates",
            "valid_timestamps",
            "has_speed",
            "has_valve_open",
            "has_battery",
            "states",
            "missing_normalized_columns",
            "available_normalized_columns",
            "data_quality",
        ]
    ).issubset(diagnostics)
    assert diagnostics["rows"] > 0
    assert "latitude" in diagnostics["columns"]
    assert diagnostics["recognized_inputs"] == {"kml": False, "csv": True, "field_data": False}
    assert diagnostics["valid_coordinates"] > 0
    assert diagnostics["valid_timestamps"] > 0
    assert diagnostics["has_speed"] is True
    assert diagnostics["has_valve_open"] is True
    assert diagnostics["has_battery"] is True
    assert isinstance(diagnostics["states"], list)
    assert diagnostics["states"]


def test_cli_diagnose_data_quality_fields(tmp_path, capsys):
    output = tmp_path / "report.html"

    main(["--csv", str(EXAMPLES / "sample_flight.csv"), "--area-ha", "12.5", "--output", str(output), "--diagnose"])
    payload = json.loads(capsys.readouterr().out)

    data_quality = payload["diagnostics"]["data_quality"]
    assert {"rows", "valid_coordinates", "valid_timestamps", "warnings_count"}.issubset(data_quality)
    assert data_quality["rows"] > 0
