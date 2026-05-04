import pandas as pd
from drone_audit.agras_metrics import calculate_real_application_rate_l_ha, calculate_spray_time_s, calculate_spray_volume_l

def test_volume_and_rate():
    df=pd.DataFrame({'volume_total_l':[1,3]})
    assert calculate_spray_volume_l(df)==2
    assert calculate_real_application_rate_l_ha(20,10)==2


def test_calculate_spray_time_with_estimated_spraying_state():
    df = pd.DataFrame({
        "timestamp": ["2026-01-01T00:00:00Z", "2026-01-01T00:00:10Z", "2026-01-01T00:00:20Z"],
        "state": ["idle", "estimated_spraying", "estimated_spraying"],
    })
    assert calculate_spray_time_s(df) == 20.0
