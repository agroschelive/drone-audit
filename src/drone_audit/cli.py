from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from drone_audit.pipeline import PipelineResult, run_pipeline
from drone_audit.schema import NORMALIZED_COLUMNS, REQUIRED_POSITION_COLUMNS


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Generate a simple auxiliary report from exported operation files.")
    p.add_argument("--kml", type=Path)
    p.add_argument("--csv", type=Path)
    p.add_argument("--xlsx", type=Path)
    p.add_argument("--txt", type=Path)
    p.add_argument("--dat", type=Path)
    p.add_argument("--planned-rate-l-ha", type=float)
    p.add_argument("--swath-width-m", type=float)
    p.add_argument("--field-data", type=Path)
    p.add_argument("--area-ha", type=float)
    p.add_argument("--output", type=Path, default=Path("reports/drone_audit_report.html"))
    p.add_argument("--diagnose", action="store_true")
    p.add_argument("--import-index", type=Path)
    p.add_argument("--no-dedupe", action="store_true")
    p.add_argument("--operation-name")
    p.add_argument("--drone-model")
    p.add_argument("--operator")
    p.add_argument("--farm-name")
    p.add_argument("--field-name")
    return p


def build_diagnostics(result: PipelineResult, args: argparse.Namespace) -> dict[str, object]:
    df = result.dataframe
    columns = [str(c) for c in df.columns]

    diagnostics: dict[str, object] = {
        "rows": int(len(df)),
        "columns": columns,
        "recognized_inputs": {
            "kml": bool(args.kml),
            "csv": bool(args.csv),
            "field_data": bool(args.field_data),
        },
        "valid_coordinates": 0,
        "valid_timestamps": 0,
        "has_speed": "speed_m_s" in df.columns,
        "has_valve_open": "valve_open" in df.columns,
        "has_battery": any(c in df.columns for c in ["battery_pct", "battery_start_pct", "battery_end_pct"]),
        "states": [],
        "source": result.metrics.get("data_source"),
    }

    diagnostics["available_normalized_columns"] = [c for c in NORMALIZED_COLUMNS if c in df.columns]
    diagnostics["missing_normalized_columns"] = [c for c in NORMALIZED_COLUMNS if c not in df.columns]

    if set(REQUIRED_POSITION_COLUMNS).issubset(df.columns):
        diagnostics["valid_coordinates"] = int(df[["latitude", "longitude"]].notna().all(axis=1).sum())

    ts_col = "timestamp" if "timestamp" in df.columns else ("timestamp_start" if "timestamp_start" in df.columns else None)
    if ts_col:
        diagnostics["valid_timestamps"] = int(pd.to_datetime(df[ts_col], errors="coerce", utc=True).notna().sum())

    if "state" in df.columns:
        diagnostics["states"] = sorted(str(s) for s in df["state"].dropna().unique())

    diagnostics["data_quality"] = {
        "rows": int(len(df)),
        "valid_coordinates": int(diagnostics["valid_coordinates"]),
        "valid_timestamps": int(diagnostics["valid_timestamps"]),
        "warnings_count": int(len(result.warnings)),
        "warnings": result.metrics.get("data_quality", []),
    }
    return diagnostics


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if not args.kml and not args.csv and not args.xlsx and not args.txt and not args.dat:
        raise SystemExit("Provide at least --kml, --csv, --xlsx, --txt or --dat.")
    result = run_pipeline(
        kml_path=args.kml,
        csv_path=args.csv,
        xlsx_path=args.xlsx,
        txt_path=args.txt,
        dat_path=args.dat,
        field_data_path=args.field_data,
        area_ha=args.area_ha,
        planned_rate_l_ha=args.planned_rate_l_ha,
        swath_width_m=args.swath_width_m,
        output_path=args.output,
        import_index_path=args.import_index,
        dedupe=not args.no_dedupe,
        operation_name=args.operation_name,
        drone_model=args.drone_model,
        operator=args.operator,
        farm_name=args.farm_name,
        field_name=args.field_name,
    )
    payload = {"metrics": result.metrics, "warnings": result.warnings, "report": str(result.report_path)}
    if args.diagnose:
        payload["diagnostics"] = build_diagnostics(result, args)
    print(json.dumps(payload, indent=2, ensure_ascii=False, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
