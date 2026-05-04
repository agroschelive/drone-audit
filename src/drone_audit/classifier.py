from __future__ import annotations

import pandas as pd
from drone_audit.spray_detector import detect_spray_on


def classify_states(df: pd.DataFrame, moving_speed_m_s: float = 0.5, spray_speed_m_s: float = 0.8) -> pd.DataFrame:
    out=df.copy()
    if "speed_m_s" not in out.columns: out["speed_m_s"]=pd.NA
    speeds=pd.to_numeric(out["speed_m_s"], errors="coerce").fillna(0.0)
    states=[]
    for i,row in out.iterrows():
        spray=detect_spray_on(row); s=float(speeds.loc[i])
        if spray is True: states.append("estimated_spraying")
        elif s<=0.3: states.append("idle")
        elif s>0.5: states.append("moving")
        else: states.append("unknown")
    out["state"]=states
    return out
