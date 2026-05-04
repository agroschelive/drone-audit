from __future__ import annotations

import pandas as pd
from drone_audit.metrics import calculate_segment_distances


def calculate_spray_volume_l(df):
    if "volume_total_l" in df:
        v = pd.to_numeric(df["volume_total_l"], errors="coerce").dropna()
        if len(v) >= 2: return float(v.iloc[-1]-v.iloc[0])
    if {"flow_l_min","timestamp"}.issubset(df.columns):
        flow = pd.to_numeric(df["flow_l_min"], errors="coerce").fillna(0)
        ts = pd.to_datetime(df["timestamp"], errors="coerce", utc=True)
        dt_min = ts.diff().dt.total_seconds().fillna(0)/60
        return float((flow*dt_min).sum())
    return None

def calculate_applied_area_ha(df):
    if "area_total_ha" in df:
        a = pd.to_numeric(df["area_total_ha"], errors="coerce").dropna()
        if len(a)>=2: return float(a.iloc[-1]-a.iloc[0])
    if "swath_width_m" in df:
        dist = float(calculate_segment_distances(df).sum())
        sw = pd.to_numeric(df["swath_width_m"], errors="coerce").mean()
        if pd.notna(sw): return float(dist*sw/10000)
    return None

def calculate_real_application_rate_l_ha(volume_l, area_ha): return None if not volume_l or not area_ha else float(volume_l/area_ha)
def calculate_swath_width_stats(df):
    if "swath_width_m" not in df: return None
    s=pd.to_numeric(df["swath_width_m"], errors="coerce")
    return {"mean": float(s.mean()), "min": float(s.min()), "max": float(s.max())} if s.notna().any() else None

def calculate_flow_stats(df):
    if "flow_l_min" not in df: return None
    s=pd.to_numeric(df["flow_l_min"], errors="coerce")
    return {"mean": float(s.mean()), "min": float(s.min()), "max": float(s.max())} if s.notna().any() else None

def calculate_battery_consumed_pct(df):
    if "battery_pct" not in df: return None
    b=pd.to_numeric(df["battery_pct"], errors="coerce").dropna()
    return float(b.iloc[0]-b.iloc[-1]) if len(b)>=2 else None

def calculate_battery_per_ha(df, area_ha):
    b=calculate_battery_consumed_pct(df); return None if b is None or not area_ha else float(b/area_ha)
def calculate_spray_time_s(df): return float(df.get("state", pd.Series(dtype=object)).eq("spraying").sum())
def calculate_non_spray_moving_time_s(df): return float(df.get("state", pd.Series(dtype=object)).eq("moving_without_spraying").sum())
def calculate_idle_time_s(df): return float(df.get("state", pd.Series(dtype=object)).eq("idle").sum())
def calculate_operational_efficiency_pct(spray_time_s, total_time_s): return None if not total_time_s else float((spray_time_s/total_time_s)*100)
def calculate_productivity_ha_h(area_ha, total_time_s): return None if not area_ha or not total_time_s else float(area_ha/(total_time_s/3600))
def calculate_spraying_productivity_ha_h(area_ha, spray_time_s): return None if not area_ha or not spray_time_s else float(area_ha/(spray_time_s/3600))
