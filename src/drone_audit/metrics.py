from __future__ import annotations

import math

import pandas as pd
from drone_audit.time_utils import total_duration_from_rows_s, calculate_row_durations_s

try:
    from pyproj import Geod
except Exception:  # pragma: no cover
    Geod = None


def haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    radius_m = 6_371_000.0
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return 2 * radius_m * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def calculate_segment_distances(df: pd.DataFrame, method: str = "haversine") -> pd.Series:
    if df.empty or {"latitude", "longitude"} - set(df.columns):
        return pd.Series(dtype="float64")

    lat = pd.to_numeric(df["latitude"], errors="coerce")
    lon = pd.to_numeric(df["longitude"], errors="coerce")
    distances = [0.0]

    for i in range(1, len(df)):
        if pd.isna(lat.iloc[i - 1]) or pd.isna(lon.iloc[i - 1]) or pd.isna(lat.iloc[i]) or pd.isna(lon.iloc[i]):
            distances.append(0.0)
            continue
        distances.append(float(haversine_m(lat.iloc[i - 1], lon.iloc[i - 1], lat.iloc[i], lon.iloc[i])))

    return pd.Series(distances, index=df.index, dtype="float64")


def total_distance_m(df: pd.DataFrame, method: str = "auto") -> float:
    if df.empty or {"latitude", "longitude"} - set(df.columns):
        return 0.0

    lat = pd.to_numeric(df["latitude"], errors="coerce")
    lon = pd.to_numeric(df["longitude"], errors="coerce")
    valid = lat.notna() & lon.notna()
    if valid.sum() < 2:
        return 0.0

    if method in {"auto", "pyproj"} and Geod is not None:
        geod = Geod(ellps="WGS84")
        return float(geod.line_length(lon[valid].tolist(), lat[valid].tolist()))

    return float(calculate_segment_distances(df, method="haversine").sum())


def total_time_s(df: pd.DataFrame) -> float | None:
    if df.empty:
        return None
    return float(total_duration_from_rows_s(df))


def derive_speed_from_track(df: pd.DataFrame) -> pd.Series:
    distances = calculate_segment_distances(df)
    if "timestamp" not in df.columns:
        return pd.Series([pd.NA] * len(df), index=df.index)
    ts = pd.to_datetime(df["timestamp"], errors="coerce", utc=True)
    dt = ts.diff().dt.total_seconds().replace(0, pd.NA)
    return distances / dt


def productivity_ha_h(area_ha: float | None, time_s: float | None) -> float | None:
    if area_ha is None or time_s is None or time_s <= 0:
        return None
    return float(area_ha) / (time_s / 3600.0)


def state_durations_s(df: pd.DataFrame) -> dict[str, float]:
    if df.empty or "state" not in df.columns:
        return {}
    row_seconds = calculate_row_durations_s(df)
    result: dict[str, float] = {}
    for state, value in row_seconds.groupby(df["state"]).sum().items():
        result[str(state)] = float(value)
    return result
