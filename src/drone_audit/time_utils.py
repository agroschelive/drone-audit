from __future__ import annotations

import pandas as pd

MAX_DELTA_S = 600.0


def calculate_row_durations_s(df: pd.DataFrame) -> pd.Series:
    if df.empty:
        return pd.Series(dtype="float64", index=df.index)
    if "timestamp" not in df.columns:
        return pd.Series(1.0, index=df.index, dtype="float64")

    ts = pd.to_datetime(df["timestamp"], errors="coerce", utc=True)
    valid = ts.notna()
    if valid.sum() < 2:
        return pd.Series(1.0, index=df.index, dtype="float64")

    ordered = ts[valid].sort_values()
    dnext = (
        (ordered.shift(-1) - ordered).dt.total_seconds().fillna(0).clip(lower=0, upper=MAX_DELTA_S)
    )
    out = pd.Series(0.0, index=df.index, dtype="float64")
    out.loc[dnext.index] = dnext.astype(float)
    return out


def total_duration_from_rows_s(df: pd.DataFrame) -> float:
    return float(calculate_row_durations_s(df).sum()) if not df.empty else 0.0


def sum_state_time_s(df: pd.DataFrame, state_name: str) -> float:
    if df.empty or "state" not in df.columns:
        return 0.0
    d = calculate_row_durations_s(df)
    return float(d[df["state"].astype("string").eq(state_name)].sum())


def sum_states_time_s(df: pd.DataFrame, state_names: set[str]) -> float:
    if df.empty or "state" not in df.columns or not state_names:
        return 0.0
    d = calculate_row_durations_s(df)
    return float(d[df["state"].astype("string").isin(state_names)].sum())
