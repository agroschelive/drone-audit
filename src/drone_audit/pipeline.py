from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from drone_audit.classifier import classify_states
from drone_audit.field_data import load_field_data
from drone_audit.metrics import derive_speed_from_track, productivity_ha_h, state_durations_s, total_distance_m, total_time_s
from drone_audit.parsers.csv_parser import parse_csv
from drone_audit.parsers.kml_parser import parse_kml
from drone_audit.report import build_html_report, write_html_report


@dataclass(frozen=True)
class PipelineResult:
    dataframe: pd.DataFrame
    metrics: dict
    warnings: list[str]
    report_path: Path | None


def _choose_base_dataframe(kml_df: pd.DataFrame | None, csv_df: pd.DataFrame | None) -> pd.DataFrame:
    if csv_df is not None and not csv_df.empty:
        if csv_df[["latitude", "longitude"]].notna().any().all():
            return csv_df.copy()
    if kml_df is not None and not kml_df.empty:
        return kml_df.copy()
    if csv_df is not None:
        return csv_df.copy()
    return pd.DataFrame()


def run_pipeline(
    kml_path: str | Path | None = None,
    csv_path: str | Path | None = None,
    field_data_path: str | Path | None = None,
    area_ha: float | None = None,
    output_path: str | Path | None = None,
) -> PipelineResult:
    warnings: list[str] = []
    kml_df = None
    csv_df = None

    if kml_path:
        parsed = parse_kml(kml_path)
        kml_df = parsed.dataframe
        warnings.extend(parsed.warnings)

    if csv_path:
        parsed = parse_csv(csv_path)
        csv_df = parsed.dataframe
        warnings.extend(parsed.warnings)

    df = _choose_base_dataframe(kml_df, csv_df)

    if df.empty:
        warnings.append("No usable data found.")
    else:
        if "speed_m_s" not in df.columns or pd.to_numeric(df.get("speed_m_s"), errors="coerce").isna().all():
            derived_speed = derive_speed_from_track(df)
            df["speed_m_s"] = derived_speed
        df = classify_states(df)

    time_s = total_time_s(df)
    metrics = {
        "distance_m": total_distance_m(df),
        "time_s": time_s,
        "area_ha": area_ha,
        "productivity_ha_h": productivity_ha_h(area_ha, time_s),
        "state_durations_s": state_durations_s(df),
    }

    field_data = load_field_data(field_data_path)
    report_path = None
    if output_path:
        html = build_html_report(df, metrics, field_data, warnings=warnings)
        report_path = write_html_report(output_path, html)

    return PipelineResult(dataframe=df, metrics=metrics, warnings=warnings, report_path=report_path)
