from __future__ import annotations

import pandas as pd


def classify_states(
    df: pd.DataFrame,
    moving_speed_m_s: float = 1.0,
    spray_speed_m_s: float = 0.8,
) -> pd.DataFrame:
    """Classify a minimal operational state.

    This is a transparent heuristic, not a definitive proof of real application.
    """
    out = df.copy()
    if "speed_m_s" not in out.columns:
        out["speed_m_s"] = pd.NA
    if "valve_open" not in out.columns:
        out["valve_open"] = None

    states: list[str] = []
    speeds = pd.to_numeric(out["speed_m_s"], errors="coerce").fillna(0.0)

    for idx, speed in speeds.items():
        valve_open = out.loc[idx, "valve_open"]
        if valve_open == True and float(speed) >= spray_speed_m_s:
            states.append("pulverizando_estimado")
        elif float(speed) >= moving_speed_m_s:
            states.append("movimento")
        else:
            states.append("ocioso")

    out["state"] = states
    return out
