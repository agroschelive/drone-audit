from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from drone_audit.privacy import sanitize_csv_dataframe
from drone_audit.tools.anonymize_csv import main


def test_sensitive_columns_removed_default():
    df = pd.DataFrame(
        {
            "Cliente": ["X"],
            "Fazenda": ["Y"],
            "Operador": ["Z"],
            "drone_serial": ["SN123"],
            "latitude": [-20.0],
            "longitude": [-49.0],
            "timestamp": ["2024-04-01T11:00:00"],
            "speed_m_s": [5.0],
            "battery_pct": [85],
            "valve_open": [True],
        }
    )
    out = sanitize_csv_dataframe(df)
    assert "Cliente" not in out.columns
    assert "Fazenda" not in out.columns
    assert "Operador" not in out.columns
    assert "drone_serial" not in out.columns
    assert "latitude" not in out.columns
    assert "longitude" not in out.columns
    assert "speed_m_s" in out.columns
    assert "battery_pct" in out.columns
    assert "valve_open" in out.columns
    assert out["timestamp"].iloc[0].startswith("2026-")


def test_fake_coordinates():
    df = pd.DataFrame({"latitude": [-19.9], "longitude": [-48.8], "speed_m_s": [1.0]})
    out = sanitize_csv_dataframe(df, fake_coordinates=True)
    assert "latitude" in out.columns and "longitude" in out.columns
    assert out["latitude"].iloc[0] != -19.9
    assert out["longitude"].iloc[0] != -48.8
    assert -23.1 < out["latitude"].iloc[0] < -22.9
    assert -51.1 < out["longitude"].iloc[0] < -50.9


def test_coordinate_aliases_removed_default_and_telemetry_preserved():
    df = pd.DataFrame(
        {
            "gps_latitude": [-22.0],
            "gps_longitude": [-51.0],
            "latitude_deg": [-22.1],
            "longitude_deg": [-51.1],
            "lat_deg": [-22.2],
            "lon_deg": [-51.2],
            "speed_m_s": [4.0],
            "altitude_m": [35.0],
            "battery_pct": [80],
        }
    )
    out = sanitize_csv_dataframe(df)
    for col in ["gps_latitude", "gps_longitude", "latitude_deg", "longitude_deg", "lat_deg", "lon_deg"]:
        assert col not in out.columns
    assert "speed_m_s" in out.columns
    assert "altitude_m" in out.columns
    assert "battery_pct" in out.columns


def test_unrelated_columns_not_removed_by_coordinate_token_logic():
    df = pd.DataFrame(
        {
            "platform": ["x"],
            "latency_ms": [10],
            "monkey_speed": [1.5],
            "speed_m_s": [4.0],
            "altitude_m": [12.0],
        }
    )
    out = sanitize_csv_dataframe(df)
    assert list(out.columns) == ["platform", "latency_ms", "monkey_speed", "speed_m_s", "altitude_m"]


def test_fake_coordinates_do_not_reuse_original_alias_values():
    df = pd.DataFrame({"gps_latitude": [-15.123], "gps_longitude": [-47.321], "speed_m_s": [1.0]})
    out = sanitize_csv_dataframe(df, fake_coordinates=True)
    assert "latitude" in out.columns and "longitude" in out.columns
    assert "gps_latitude" not in out.columns and "gps_longitude" not in out.columns
    assert -23.1 < out["latitude"].iloc[0] < -22.9
    assert -51.1 < out["longitude"].iloc[0] < -50.9
    assert out["latitude"].iloc[0] != -15.123
    assert out["longitude"].iloc[0] != -47.321


def test_timestamp_normalization():
    df = pd.DataFrame({"timestamp": ["2024-07-13 12:00:00", "2024-07-13 12:00:05"]})
    out = sanitize_csv_dataframe(df)
    assert out["timestamp"].iloc[0].startswith("2026-01-01")
    assert out["timestamp"].iloc[0].endswith("Z")
    assert "2024" not in " ".join(out["timestamp"].tolist())


def test_timestamp_aliases_normalized():
    df = pd.DataFrame(
        {
            "gps_time": ["2024-07-13 12:00:00"],
            "recorded_at": ["2025-02-01 01:02:03"],
            "created_at": ["2023-01-01 00:00:01"],
        }
    )
    out = sanitize_csv_dataframe(df)
    for col in ["gps_time", "recorded_at", "created_at"]:
        assert out[col].iloc[0].startswith("2026-01-01")
        assert out[col].iloc[0].endswith("Z")
    assert "2024" not in " ".join(out["gps_time"].tolist())


def test_relative_duration_columns_not_normalized():
    df = pd.DataFrame({"time_s": [1.0], "elapsed_s": [2.0], "elapsed_time_s": [3.0], "duration_s": [4.0]})
    out = sanitize_csv_dataframe(df)
    assert out["time_s"].tolist() == [1.0]
    assert out["elapsed_s"].tolist() == [2.0]
    assert out["elapsed_time_s"].tolist() == [3.0]
    assert out["duration_s"].tolist() == [4.0]


def test_sensitive_key_detection():
    df = pd.DataFrame(
        {
            "api_key": ["a"],
            "secret_key": ["b"],
            "access_key": ["c"],
            "private_key": ["d"],
            "public_key": ["e"],
            "credential_key": ["f"],
            "token_key": ["g"],
            "monkey_speed": [1.1],
            "speed_m_s": [2.2],
        }
    )
    out = sanitize_csv_dataframe(df)
    for col in [
        "api_key",
        "secret_key",
        "access_key",
        "private_key",
        "public_key",
        "credential_key",
        "token_key",
    ]:
        assert col not in out.columns
    assert "monkey_speed" in out.columns
    assert "speed_m_s" in out.columns


def test_cli_summary(tmp_path, capsys):
    inp = tmp_path / "in.csv"
    outp = tmp_path / "out.csv"
    pd.DataFrame({"Cliente": ["a"], "latitude": [1.0], "speed_m_s": [3.0]}).to_csv(inp, index=False)
    rc = main(["--input", str(inp), "--output", str(outp)])
    assert rc == 0
    assert outp.exists()
    summary = json.loads(capsys.readouterr().out)
    assert summary["rows"] == 1
    assert "columns_before" in summary and "columns_after" in summary
    assert "original_coordinates_removed" in summary
    assert "synthetic_coordinates_added" in summary
    assert summary["original_coordinates_removed"] is True
    assert summary["synthetic_coordinates_added"] is False
    result = pd.read_csv(outp)
    assert "Cliente" not in result.columns
    assert "latitude" not in result.columns


def test_docs_presence_and_privacy_text():
    required = [
        "SECURITY.md",
        "CONTRIBUTING.md",
        "CHANGELOG.md",
        "examples/real_samples/README.md",
        "docs/audit-rules.md",
    ]
    for path in required:
        assert Path(path).exists()

    security = Path("SECURITY.md").read_text(encoding="utf-8").lower()
    readme = Path("README.md").read_text(encoding="utf-8").lower()
    expected = Path("docs/expected-real-files.md").read_text(encoding="utf-8").lower()
    development = Path("docs/development.md").read_text(encoding="utf-8").lower()
    arch = Path("docs/architecture.md").read_text(encoding="utf-8").lower()
    rules = Path("docs/audit-rules.md").read_text(encoding="utf-8").lower()

    assert "real coordinates" in security
    assert "security.md" in readme
    assert "docs/audit-rules.md" in readme
    assert "do not commit real coordinates" in expected
    assert "inspect sanitized output before publishing" in security or "inspect sanitized output before publishing" in expected
    assert "docs/audit-rules.md" in development
    assert "speed_m_s" in rules
    assert "valve_open" in rules
    assert "estimated_spraying" in rules
    assert "heuristic" in rules or "experimental" in rules
    assert "not proof of real spraying" in rules or "not proof of real spraying/application" in rules

    banned_pt = [
        "arquivos reais esperados",
        "desenvolvimento",
        "arquitetura",
        "objetivo",
        "rodar testes",
        "cuidados com dados sensíveis",
    ]
    for term in banned_pt:
        assert term not in development
        assert term not in arch
        assert term not in expected
