from __future__ import annotations

import pandas as pd

from drone_audit.spray_detector import detect_spray_on
from drone_audit.states import STATE_IDLE, STATE_MOVING, STATE_SPRAYING, STATE_UNKNOWN


def classify_states(
    df: pd.DataFrame,
    moving_speed_m_s: float = 0.5,
    spray_speed_m_s: float = 0.8,
) -> pd.DataFrame:
    out = df.copy()
    if "speed_m_s" not in out.columns:
        out["speed_m_s"] = pd.NA

    speeds = pd.to_numeric(out["speed_m_s"], errors="coerce").fillna(0.0)
    states: list[str] = []

    for i, row in out.iterrows():
        spray = detect_spray_on(row)
        speed = float(speeds.loc[i])
        if spray is True and speed >= spray_speed_m_s:
            states.append(STATE_SPRAYING)
        elif speed <= 0.3:
            states.append(STATE_IDLE)
        elif speed > moving_speed_m_s:
            states.append(STATE_MOVING)
        else:
            states.append(STATE_UNKNOWN)

    out["state"] = states
    return out
