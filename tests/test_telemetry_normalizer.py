import pandas as pd
from drone_audit.telemetry_normalizer import normalize_telemetry_dataframe

def test_normalize_cols():
    df=pd.DataFrame({"time":["2026-01-01"],"lat":[1],"lon":[2],"flow":["1,5"]})
    out,w=normalize_telemetry_dataframe(df,"txt")
    assert "timestamp" in out and out["flow_l_min"].iloc[0]==1.5
