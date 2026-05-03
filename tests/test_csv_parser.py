from drone_audit.parsers.csv_parser import parse_csv
from conftest import EXAMPLES


def test_parse_csv():
    parsed = parse_csv(EXAMPLES / "sample_flight.csv")
    df = parsed.dataframe
    assert len(df) == 5
    assert df["latitude"].notna().all()
    assert df["valve_open"].tolist()[1] is True


def test_parse_csv_with_corrupted_and_missing_fields(tmp_path):
    csv_path = tmp_path / "aggressive.csv"
    csv_path.write_text(
        "\n".join(
            [
                "timestamp,latitude,longitude,speed_kmh,valve_open",
                "2026-01-01T00:00:00Z,-23.55,-46.63,18,true",
                "not-a-date,-23.56,-46.64,15,false",
                "2026-01-01T00:00:20Z,999,-46.65,20,yes",
                "2026-01-01T00:00:30Z,-23.57,-190,12,no",
                "2026-01-01T00:00:40Z,-23.58,-46.66,10,maybe",
                "broken,with,too,many,columns,ignored",
            ]
        ),
        encoding="utf-8",
    )

    parsed = parse_csv(csv_path)
    df = parsed.dataframe
    assert len(df) == 5
    assert any("invalid timestamps" in msg for msg in parsed.warnings)
    assert any("out-of-range coordinates" in msg for msg in parsed.warnings)
    assert df["timestamp"].isna().sum() == 1
    assert df["latitude"].isna().sum() == 2


def test_parse_csv_without_coordinates(tmp_path):
    csv_path = tmp_path / "missing_coords.csv"
    csv_path.write_text(
        "timestamp,speed_m_s,valve_open\n2026-01-01T00:00:00Z,2.0,true\n",
        encoding="utf-8",
    )

    parsed = parse_csv(csv_path)
    assert any("latitude/longitude" in msg for msg in parsed.warnings)
