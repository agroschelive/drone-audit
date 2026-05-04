import pandas as pd
from drone_audit.spray_detector import detect_spray_on, detect_spray_anomalies

def test_detect_sources():
    assert detect_spray_on({"spray_on":"sim"}) is True
    assert detect_spray_on({"valve_open":"aberto"}) is True
    assert detect_spray_on({"flow_l_min":1}) is True

def test_volume_sem_movimento():
    df=pd.DataFrame({"speed_m_s":[0.1,0.1],"volume_total_l":[1.0,1.01],"spray_on":[True,True],"flow_l_min":[0,0]})
    codes={a['code'] for a in detect_spray_anomalies(df)}
    assert "volume_sem_movimento" in codes and "pulverizacao_sem_fluxo" in codes
