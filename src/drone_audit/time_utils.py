from __future__ import annotations

import pandas as pd

MAX_DELTA_S = 600.0


def calculate_row_durations_s(df: pd.DataFrame) -> pd.Series:
    if df.empty:
        return pd.Series(dtype="float64", index=df.index)

    if "timestamp" not in df.columns:
        return pd.Series(1.0, index=df.index, dtype="float64")

    ts = pd.to_datetime(df["timestamp"], errors="coerce", utc=True)
    if ts.notna().sum() < 2:
        return pd.Series(1.0, index=df.index, dtype="float64")

    ordered = ts.sort_values()
    deltas = ordered.diff().dt.total_seconds()
    deltas = deltas.mask(deltas < 0, 0)
    deltas = deltas.clip(upper=MAX_DELTA_S)
    first_delta = 0.0
    deltas.iloc[0] = first_delta
    deltas = deltas.fillna(first_delta)
    durations = deltas.reindex(df.index).fillna(first_delta)
    return durations.astype("float64")


def sum_state_time_s(df: pd.DataFrame, state_name: str) -> float:
    if df.empty or "state" not in df.columns:
        return 0.0
    durations = calculate_row_durations_s(df)
    mask = df["state"].astype("string").eq(state_name)
    return float(durations[mask].sum())


def total_duration_from_rows_s(df: pd.DataFrame) -> float:
    if df.empty:
        return 0.0
    return float(calculate_row_durations_s(df).sum())
