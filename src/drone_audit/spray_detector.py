from __future__ import annotations
import pandas as pd
from drone_audit.agras_telemetry import AgrasSpraySegment
from drone_audit.metrics import calculate_segment_distances


def _as_bool(value):
    if isinstance(value, bool):
        return value
    if value is None or pd.isna(value):
        return None
    s = str(value).strip().lower()
    s = s.replace("não", "nao")
    t = {"true", "1", "yes", "sim", "on", "aberto", "ligado"}
    f = {"false", "0", "no", "nao", "off", "fechado", "desligado"}
    if s in t:
        return True
    if s in f:
        return False
    return None


def detect_spray_on(row) -> bool | None:
    for col in ["spray_on", "valve_open", "pump_on"]:
        b = _as_bool(row.get(col))
        if b is not None:
            return b
    flow = pd.to_numeric(pd.Series([row.get("flow_l_min")]), errors="coerce").iloc[0]
    if pd.notna(flow) and float(flow) > 0:
        return True
    if bool(row.get("_volume_increase", False)) or bool(row.get("_area_increase", False)):
        return True
    return None


def _delta(series):
    s = pd.to_numeric(series, errors="coerce").dropna()
    return float(s.iloc[-1] - s.iloc[0]) if len(s) >= 2 else None


def create_spray_segments(df):
    if df.empty:
        return []
    d = df.copy()
    d["_volume_increase"] = (
        pd.to_numeric(d.get("volume_total_l"), errors="coerce").diff().fillna(0) > 0.001
    )
    d["_area_increase"] = (
        pd.to_numeric(d.get("area_total_ha"), errors="coerce").diff().fillna(0) > 0.00001
    )
    d["_spray"] = d.apply(detect_spray_on, axis=1).replace({None: False}).astype(bool)
    d["_dist"] = calculate_segment_distances(d)
    seg = []
    start = None
    for i, on in enumerate(d["_spray"].tolist() + [False]):
        if on and start is None:
            start = i
        if (not on) and start is not None:
            part = d.iloc[start:i]
            ts = pd.to_datetime(part.get("timestamp"), errors="coerce", utc=True)
            duration = (
                float((ts.max() - ts.min()).total_seconds())
                if ts.notna().sum() >= 2
                else float(i - start)
            )
            seg.append(
                AgrasSpraySegment(
                    ts.min() if ts.notna().any() else start,
                    ts.max() if ts.notna().any() else i - 1,
                    duration,
                    start,
                    i - 1,
                    _delta(part.get("volume_total_l")),
                    _delta(part.get("area_total_ha")),
                    float(pd.to_numeric(part.get("_dist"), errors="coerce").sum()),
                    pd.to_numeric(part.get("flow_l_min"), errors="coerce").mean()
                    if "flow_l_min" in part
                    else None,
                    pd.to_numeric(part.get("speed_m_s"), errors="coerce").mean()
                    if "speed_m_s" in part
                    else None,
                    pd.to_numeric(part.get("swath_width_m"), errors="coerce").mean()
                    if "swath_width_m" in part
                    else None,
                )
            )
            start = None
    return seg


def detect_spray_anomalies(df):
    alerts = []
    if df.empty:
        return [{"code": "dados_insuficientes_spray"}]
    d = df.copy()
    vol = (
        d["volume_total_l"] if "volume_total_l" in d else pd.Series(index=d.index, dtype="float64")
    )
    area = d["area_total_ha"] if "area_total_ha" in d else pd.Series(index=d.index, dtype="float64")
    d["_volume_increase"] = pd.to_numeric(vol, errors="coerce").diff().fillna(0) > 0.001
    d["_area_increase"] = pd.to_numeric(area, errors="coerce").diff().fillna(0) > 0.00001
    d["_spray"] = d.apply(detect_spray_on, axis=1)
    speed = pd.to_numeric(d.get("speed_m_s"), errors="coerce").fillna(0)
    spray = d["_spray"].replace({None: False}).astype(bool)
    if d["_spray"].isna().all():
        alerts.append({"code": "dados_insuficientes_spray"})
    if (spray & (speed < 0.3)).any():
        alerts.append({"code": "spray_ligado_parado"})
    moving_without_spray = ((~spray) & (speed > 0.5))
    if moving_without_spray.any():
        valid_rows = int(d["_spray"].notna().sum())
        point_ratio = (float(moving_without_spray.sum()) / valid_rows) if valid_rows > 0 else 0.0
        time_ratio = 0.0
        if "timestamp" in d.columns:
            ts = pd.to_datetime(d["timestamp"], errors="coerce", utc=True)
            if ts.notna().sum() >= 2:
                dt = ts.sort_values().diff().dt.total_seconds().clip(lower=0, upper=600).fillna(0)
                row_durations = dt.reindex(d.index).fillna(0)
                total_time = float(row_durations.sum())
                moving_time = float(row_durations[moving_without_spray].sum())
                time_ratio = (moving_time / total_time) if total_time > 0 else 0.0
        if point_ratio > 0.2 or time_ratio > 0.2:
            alerts.append({"code": "deslocando_sem_pulverizar"})
    if (d["_volume_increase"] & (speed < 0.3)).any():
        alerts.append({"code": "volume_sem_movimento"})
    flow_series = pd.to_numeric(d.get("flow_l_min", pd.Series(index=d.index, dtype="float64")), errors="coerce").fillna(0)
    if ((spray) & (flow_series <= 0)).any():
        alerts.append({"code": "pulverizacao_sem_fluxo"})
    if ((speed > 1.0) & (~spray) & (d["_area_increase"])).any():
        alerts.append({"code": "falha_pulverizacao_em_movimento", "severity": "warning"})
    if "flow_l_min" in d:
        std = pd.to_numeric(d["flow_l_min"], errors="coerce").std()
        if pd.notna(std) and std > 5:
            alerts.append({"code": "vazao_instavel"})
    if (
        "swath_width_m" not in d
        or pd.to_numeric(d.get("swath_width_m"), errors="coerce").isna().all()
    ):
        alerts.append({"code": "pulverizacao_sem_largura_faixa"})
    return alerts
