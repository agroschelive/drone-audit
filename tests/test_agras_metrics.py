import pandas as pd
from drone_audit.agras_metrics import calculate_spray_volume_l, calculate_real_application_rate_l_ha

def test_volume_and_rate():
    df=pd.DataFrame({'volume_total_l':[1,3]})
    assert calculate_spray_volume_l(df)==2
    assert calculate_real_application_rate_l_ha(20,10)==2
