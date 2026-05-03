from drone_audit.parsers.kml_parser import parse_kml
from conftest import EXAMPLES


def test_parse_linestring_kml():
    parsed = parse_kml(EXAMPLES / "sample_route.kml")
    assert len(parsed.dataframe) == 4
    assert {"latitude", "longitude"}.issubset(parsed.dataframe.columns)


def test_parse_gx_track_kml():
    parsed = parse_kml(EXAMPLES / "sample_track_gx.kml")
    assert len(parsed.dataframe) == 3
    assert parsed.dataframe["timestamp"].notna().all()
