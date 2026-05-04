import pandas as pd
from drone_audit.data_quality import assess_data_quality


def test_assess_data_quality_warns_missing():
    df = pd.DataFrame({'latitude':[-23.0],'longitude':[-46.0]})
    w = assess_data_quality(df,'kml')
    assert 'sem_timestamps' in w
    assert 'sem_bateria' in w
