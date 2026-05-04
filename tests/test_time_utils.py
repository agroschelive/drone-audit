import pandas as pd
from drone_audit.time_utils import calculate_row_durations_s, total_duration_from_rows_s

def test_duration_with_timestamp():
    df=pd.DataFrame({"timestamp":["2026-01-01T00:00:00Z","2026-01-01T00:00:02Z","2026-01-01T00:00:05Z"]})
    assert total_duration_from_rows_s(df)==5.0

def test_duration_without_timestamp():
    df=pd.DataFrame({"a":[1,2,3]})
    assert total_duration_from_rows_s(df)==3.0

def test_out_of_order_timestamp():
    df=pd.DataFrame({"timestamp":["2026-01-01T00:00:03Z","2026-01-01T00:00:00Z","2026-01-01T00:00:02Z"]})
    d=calculate_row_durations_s(df)
    assert d.sum()>=2
