from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from drone_audit.classifier import classify_states
from drone_audit.data_quality import assess_data_quality
from drone_audit.diagnostics import diagnose_operational
from drone_audit.field_data import load_field_data
from drone_audit.metrics import derive_speed_from_track, productivity_ha_h, state_durations_s, total_distance_m, total_time_s
from drone_audit.operations import battery_usage_pct, compute_operational_metrics, generate_operational_alerts
from drone_audit.parsers.csv_parser import parse_csv
from drone_audit.parsers.kml_parser import parse_kml
from drone_audit.parsers.xlsx_parser import parse_xlsx
from drone_audit.report import build_html_report, write_html_report
from drone_audit.storage import DEFAULT_IMPORT_INDEX, file_sha256, is_duplicate_file, load_import_index, register_import, save_import_index


@dataclass(frozen=True)
class PipelineResult:
    dataframe: pd.DataFrame
    metrics: dict
    warnings: list[str]
    report_path: Path | None


def _choose_base_dataframe(kml_df: pd.DataFrame | None, csv_df: pd.DataFrame | None) -> pd.DataFrame:
    if csv_df is not None and not csv_df.empty:
        if {"latitude", "longitude"}.issubset(csv_df.columns) and csv_df[["latitude", "longitude"]].notna().any().all():
            return csv_df.copy()
    if kml_df is not None and not kml_df.empty:
        return kml_df.copy()
    if csv_df is not None:
        return csv_df.copy()
    return pd.DataFrame()


def run_pipeline(kml_path=None, csv_path=None, field_data_path=None, xlsx_path=None, import_index_path=None, dedupe: bool = True,
                 operation_name: str | None = None, drone_model: str | None = None, operator: str | None = None,
                 farm_name: str | None = None, field_name: str | None = None, area_ha: float | None = None, output_path=None) -> PipelineResult:
    warnings: list[str] = []
    kml_df = csv_df = xlsx_df = None
    source_type = "unknown"

    if kml_path:
        parsed = parse_kml(kml_path)
        kml_df = parsed.dataframe
        warnings.extend(parsed.warnings)
        source_type = "kml"
    if csv_path:
        parsed = parse_csv(csv_path)
        csv_df = parsed.dataframe
        warnings.extend(parsed.warnings)
        source_type = "csv"
    if xlsx_path:
        if dedupe:
            idx_path = Path(import_index_path) if import_index_path else DEFAULT_IMPORT_INDEX
            idx = load_import_index(idx_path)
            h = file_sha256(xlsx_path)
            if is_duplicate_file(h, idx):
                warnings.append("arquivo_duplicado")
            else:
                save_import_index(idx_path, register_import(h, {"path": str(xlsx_path)}, idx))
        parsed = parse_xlsx(xlsx_path)
        xlsx_df = parsed.dataframe
        warnings.extend(parsed.warnings)
        source_type = parsed.source_type

    df = xlsx_df.copy() if xlsx_df is not None else _choose_base_dataframe(kml_df, csv_df)
    if df.empty:
        warnings.append("No usable data found.")
    else:
        if "speed_m_s" not in df.columns or pd.to_numeric(df.get("speed_m_s"), errors="coerce").isna().all():
            df["speed_m_s"] = derive_speed_from_track(df)
        df = classify_states(df)

    time_s = total_time_s(df)
    durations = state_durations_s(df)
    volume_aplicado_l = float(pd.to_numeric(df.get("volume_l"), errors="coerce").fillna(0).sum()) if "volume_l" in df.columns else None
    battery_usage = battery_usage_pct(df)
    op_metrics = compute_operational_metrics(durations, area_ha, time_s, battery_usage, volume_aplicado_l)
    dq = assess_data_quality(df, source_type) if not df.empty else ["dados_insuficientes_para_estado_operacional"]
    warnings.extend(dq)

    metrics = {
        "distance_m": total_distance_m(df), "time_s": time_s, "area_ha": area_ha,
        "productivity_ha_h": productivity_ha_h(area_ha, time_s), "state_durations_s": durations,
        "battery_usage_pct": battery_usage, "volume_aplicado_l": volume_aplicado_l,
        "operational": op_metrics.__dict__, "operational_alerts": generate_operational_alerts(op_metrics),
        "diagnostics_auto": diagnose_operational({"operational": op_metrics.__dict__}, dq),
        "data_source": source_type, "data_quality": dq,
        "operation_name": operation_name, "drone_model": drone_model, "operator": operator,
        "farm_name": farm_name, "field_name": field_name,
    }

    field_data = load_field_data(field_data_path)
    report_path = None
    if output_path:
        html = build_html_report(df, metrics, field_data, warnings=warnings)
        report_path = write_html_report(output_path, html)
    return PipelineResult(dataframe=df, metrics=metrics, warnings=warnings, report_path=report_path)
