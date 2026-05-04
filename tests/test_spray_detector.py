import pandas as pd
from drone_audit.spray_detector import detect_spray_on

def test_detect_by_flow():
    assert detect_spray_on(pd.Series({'flow_l_min':1.0})) is True
