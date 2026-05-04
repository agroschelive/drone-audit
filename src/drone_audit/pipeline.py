from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import pandas as pd
from drone_audit.classifier import classify_states
from drone_audit.data_quality import assess_data_quality
from drone_audit.diagnostics import diagnose_operational
from drone_audit.field_data import load_field_data
from drone_audit.metrics import (
    derive_speed_from_track,
    productivity_ha_h,
    state_durations_s,
    total_distance_m,
    total_time_s,
)
from drone_audit.operations import (
    battery_usage_pct,
    compute_operational_metrics,
    generate_operational_alerts,
)
from drone_audit.parsers.csv_parser import parse_csv
from drone_audit.parsers.kml_parser import parse_kml
from drone_audit.parsers.xlsx_parser import parse_xlsx
from drone_audit.parsers.txt_parser import parse_txt
from drone_audit.parsers.dat_parser import parse_dat
from drone_audit.telemetry_normalizer import normalize_telemetry_dataframe
from drone_audit.spray_detector import create_spray_segments, detect_spray_anomalies
from drone_audit.agras_metrics import (
    calculate_spray_volume_l,
    calculate_applied_area_ha,
    calculate_real_application_rate_l_ha,
    calculate_flow_stats,
    calculate_swath_width_stats,
    calculate_battery_per_ha,
    calculate_spray_time_s,
    calculate_non_spray_moving_time_s,
    calculate_idle_time_s,
)
from drone_audit.report import build_html_report, write_html_report
from drone_audit.storage import (
    DEFAULT_IMPORT_INDEX,
    file_sha256,
    is_duplicate_file,
    load_import_index,
    register_import,
    save_import_index,
)


@dataclass(frozen=True)
class PipelineResult:
    dataframe: pd.DataFrame
    metrics: dict
    warnings: list[str]
    report_path: Path | None


def _select_primary_source(txt_df, csv_df, kml_df, xlsx_df, has_dat: bool):
    w = []

    def has_coords(d):
        return (
            d is not None
            and not d.empty
            and {"latitude", "longitude"}.issubset(d.columns)
            and d[["latitude", "longitude"]].notna().any().all()
        )

    if txt_df is not None and not txt_df.empty:
        return txt_df.copy(), "txt", w
    if has_coords(csv_df):
        return csv_df.copy(), "csv", w
    if has_coords(kml_df):
        return kml_df.copy(), "kml", w
    if xlsx_df is not None and not xlsx_df.empty:
        return (
            xlsx_df.copy(),
            "xlsx_smartfarm",
            ["xlsx_resumo_operacional_experimental", "fonte_sem_telemetria_ponto_a_ponto"],
        )
    if csv_df is not None and not csv_df.empty:
        return csv_df.copy(), "csv", ["fonte_sem_telemetria_ponto_a_ponto"]
    if has_dat:
        return pd.DataFrame(), "dat", ["formato_dat_nao_suportado"]
    return pd.DataFrame(), "unknown", ["fonte_vazia"]


def run_pipeline(**kwargs) -> PipelineResult:
    kml_path = kwargs.get("kml_path")
    csv_path = kwargs.get("csv_path")
    field_data_path = kwargs.get("field_data_path")
    xlsx_path = kwargs.get("xlsx_path")
    txt_path = kwargs.get("txt_path")
    dat_path = kwargs.get("dat_path")
    import_index_path = kwargs.get("import_index_path")
    dedupe = kwargs.get("dedupe", True)
    operation_name = kwargs.get("operation_name")
    drone_model = kwargs.get("drone_model")
    operator = kwargs.get("operator")
    farm_name = kwargs.get("farm_name")
    field_name = kwargs.get("field_name")
    area_ha = kwargs.get("area_ha")
    planned_rate_l_ha = kwargs.get("planned_rate_l_ha")
    swath_width_m = kwargs.get("swath_width_m")
    output_path = kwargs.get("output_path")
    warnings = []
    kml_df = csv_df = xlsx_df = txt_df = None
    xlsx_summary = {}
    if kml_path:
        p = parse_kml(kml_path)
        kml_df = p.dataframe
        warnings.extend(p.warnings)
    if csv_path:
        p = parse_csv(csv_path)
        csv_df = p.dataframe
        warnings.extend(p.warnings)
    if txt_path:
        p = parse_txt(txt_path)
        txt_df = p.dataframe
        warnings.extend(p.warnings)
    if dat_path:
        warnings.extend(parse_dat(dat_path).warnings)
    if xlsx_path:
        if dedupe:
            idx_path = Path(import_index_path) if import_index_path else DEFAULT_IMPORT_INDEX
            idx = load_import_index(idx_path)
            h = file_sha256(xlsx_path)
            if is_duplicate_file(h, idx):
                warnings.append("arquivo_duplicado")
            else:
                save_import_index(idx_path, register_import(h, {"path": str(xlsx_path)}, idx))
        p = parse_xlsx(xlsx_path)
        xlsx_df = p.dataframe
        warnings.extend(p.warnings)
        if not xlsx_df.empty:
            row = xlsx_df.iloc[0]
            for k in [
                "duration_s",
                "area_ha",
                "distance_m",
                "volume_l",
                "application_rate_l_ha",
                "battery_start_pct",
                "battery_end_pct",
                "battery_consumed_pct",
            ]:
                if k in xlsx_df.columns and pd.notna(row.get(k)):
                    xlsx_summary[k] = float(row[k])
    df, source_type, source_w = _select_primary_source(
        txt_df, csv_df, kml_df, xlsx_df, bool(dat_path)
    )
    warnings.extend(source_w)
    if not df.empty and source_type != "xlsx_smartfarm":
        df, _wn = normalize_telemetry_dataframe(df, source_type)
        warnings.extend(_wn)
    if df.empty and source_type != "dat":
        warnings.append("No usable data found.")
    elif not df.empty and source_type != "xlsx_smartfarm":
        if swath_width_m is not None:
            df["swath_width_m"] = df.get("swath_width_m", pd.Series(index=df.index)).fillna(
                swath_width_m
            )
        if (
            "speed_m_s" not in df.columns
            or pd.to_numeric(df.get("speed_m_s"), errors="coerce").isna().all()
        ):
            df["speed_m_s"] = derive_speed_from_track(df)
        df = classify_states(df)
    time_s = xlsx_summary.get("duration_s") if source_type == "xlsx_smartfarm" else total_time_s(df)
    durations = {} if source_type == "xlsx_smartfarm" else state_durations_s(df)
    volume_aplicado_l = (
        xlsx_summary.get("volume_l")
        if source_type == "xlsx_smartfarm"
        else calculate_spray_volume_l(df)
    )
    battery_usage = (
        xlsx_summary.get("battery_consumed_pct")
        if source_type == "xlsx_smartfarm"
        else battery_usage_pct(df)
    )
    applied_area = (
        xlsx_summary.get("area_ha")
        if source_type == "xlsx_smartfarm"
        else calculate_applied_area_ha(df)
    )
    effective_area_ha = area_ha if area_ha is not None else applied_area
    dq = (
        assess_data_quality(df, source_type)
        if not df.empty
        else ["dados_insuficientes_para_estado_operacional"]
    )
    warnings.extend(dq)
    op_metrics = compute_operational_metrics(
        durations, effective_area_ha, time_s, battery_usage, volume_aplicado_l
    )
    metrics = {
        "distance_m": xlsx_summary.get("distance_m", total_distance_m(df)),
        "time_s": time_s,
        "area_ha": area_ha,
        "effective_area_ha": effective_area_ha,
        "productivity_ha_h": productivity_ha_h(effective_area_ha, time_s),
        "state_durations_s": durations,
        "battery_usage_pct": battery_usage,
        "volume_aplicado_l": volume_aplicado_l,
        "applied_area_ha": applied_area,
        "real_rate_l_ha": xlsx_summary.get(
            "application_rate_l_ha",
            calculate_real_application_rate_l_ha(volume_aplicado_l, applied_area),
        ),
        "operational": op_metrics.__dict__,
        "operational_alerts": generate_operational_alerts(op_metrics),
        "spray_segments": [s.__dict__ for s in create_spray_segments(df)],
        "spray_anomalies": detect_spray_anomalies(df),
        "flow_stats": calculate_flow_stats(df),
        "swath_width_stats": calculate_swath_width_stats(df),
        "battery_per_ha_pct": calculate_battery_per_ha(df, effective_area_ha),
        "spray_time_s": calculate_spray_time_s(df),
        "non_spray_moving_time_s": calculate_non_spray_moving_time_s(df),
        "idle_time_s": calculate_idle_time_s(df),
        "diagnostics_auto": diagnose_operational(
            {"operational": op_metrics.__dict__}, dq, [], planned_rate_l_ha
        ),
        "data_source": source_type,
        "data_quality": dq,
        "operation_name": operation_name,
        "drone_model": drone_model,
        "operator": operator,
        "farm_name": farm_name,
        "field_name": field_name,
    }
    field_data = load_field_data(field_data_path)
    report_path = None
    if output_path:
        report_path = write_html_report(
            output_path, build_html_report(df, metrics, field_data, warnings=warnings)
        )
    return PipelineResult(df, metrics, warnings, report_path)
