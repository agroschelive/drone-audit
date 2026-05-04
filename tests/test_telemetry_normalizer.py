import pandas as pd
from drone_audit.telemetry_normalizer import normalize_telemetry_dataframe

def test_conversions_and_aliases():
    df=pd.DataFrame({"data_hora":["2026-01-01T00:00:00Z"],"lat":[1],"lon":[2],"vazao":["1,5"],"bateria":["87%"],"speed_km/h":["36"],"volume_ml":["1500"],"area_m²":["10000"],"pulverizador_ligado":["sim"]})
    out,_=normalize_telemetry_dataframe(df,"txt")
    assert out["flow_l_min"].iloc[0]==1.5
    assert out["battery_pct"].iloc[0]==87
    assert out["speed_m_s"].iloc[0]==10
    assert out["volume_total_l"].iloc[0]==1.5
    assert out["area_total_ha"].iloc[0]==1
    assert bool(out["spray_on"].iloc[0]) is True
