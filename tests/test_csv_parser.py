from drone_audit.parsers.csv_parser import parse_csv
from conftest import EXAMPLES


def test_parse_csv():
    parsed = parse_csv(EXAMPLES / "sample_flight.csv")
    df = parsed.dataframe
    assert len(df) == 5
    assert df["latitude"].notna().all()
    assert df["valve_open"].tolist()[1] is True
