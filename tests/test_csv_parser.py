from drone_audit.parsers.csv_parser import parse_csv
from conftest import EXAMPLES


def test_parse_csv():
    parsed = parse_csv(EXAMPLES / "sample_flight.csv")
    df = parsed.dataframe
    assert len(df) == 5
    assert df["latitude"].notna().all()
    assert df["valve_open"].tolist()[1] is True


def test_parse_csv_corrupted_and_out_of_range_values(tmp_path):
    csv_path = tmp_path / "corrupted.csv"
    csv_path.write_text(
        "timestamp,latitude,longitude,speed_kmh\n"
        "2024-01-01T10:00:00Z,-22.0,-47.0,10\n"
        "not-a-date,200,-47.1,12\n"
        "2024-01-01T10:02:00Z,-22.1,-190,13\n",
        encoding="utf-8",
    )

    parsed = parse_csv(csv_path)
    df = parsed.dataframe

    assert df["timestamp"].isna().sum() == 1
    assert df["latitude"].isna().sum() == 1
    assert df["longitude"].isna().sum() == 1
    assert any("invalid timestamp" in warning for warning in parsed.warnings)
    assert any("latitude out of range" in warning for warning in parsed.warnings)
    assert any("longitude out of range" in warning for warning in parsed.warnings)


def test_parse_csv_missing_columns(tmp_path):
    csv_path = tmp_path / "missing_columns.csv"
    csv_path.write_text(
        "foo,bar\n"
        "1,2\n",
        encoding="utf-8",
    )

    parsed = parse_csv(csv_path)

    assert any("latitude/longitude" in warning for warning in parsed.warnings)
    assert any("timestamp column" in warning for warning in parsed.warnings)
    assert any("speed column" in warning for warning in parsed.warnings)
