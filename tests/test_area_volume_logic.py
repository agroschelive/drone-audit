import pandas as pd
from drone_audit.agras_metrics import calculate_applied_area_ha

def test_swath_uses_only_spraying_segments():
    df = pd.DataFrame({
        "latitude":[-23.0,-23.0,-23.0], "longitude":[-46.0,-45.999,-45.998],
        "swath_width_m":[10,10,10], "state":["estimated_spraying","estimated_spraying","transit"]
    })
    area = calculate_applied_area_ha(df)
    assert area is not None and area > 0
