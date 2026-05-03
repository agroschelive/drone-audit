from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from drone_audit.pipeline import PipelineResult, run_pipeline
from drone_audit.schema import NORMALIZED_COLUMNS, REQUIRED_POSITION_COLUMNS


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate a simple auxiliary report from exported operation files.")
    parser.add_argument("--kml", type=Path, help="Path to a KML file.")
    parser.add_argument("--csv", type=Path, help="Path to a CSV file.")
    parser.add_argument("--field-data", type=Path, help="Optional JSON with complementary field data.")
    parser.add_argument("--area-ha", type=float, help="Optional operated area in hectares.")
    parser.add_argument("--output", type=Path, default=Path("reports/drone_audit_report.html"), help="Output HTML report path.")
    parser.add_argument("--diagnose", action="store_true", help="Include diagnostic metadata in JSON output.")
    return parser


def build_diagnostics(result: PipelineResult, args: argparse.Namespace) -> dict[str, object]:
    df = result.dataframe
    columns = [str(col) for col in df.columns]

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
        "has_battery": "battery_pct" in df.columns,
        "states": [],
    }

    available_normalized_columns = [col for col in NORMALIZED_COLUMNS if col in df.columns]
    missing_normalized_columns = [col for col in NORMALIZED_COLUMNS if col not in df.columns]

    diagnostics["available_normalized_columns"] = available_normalized_columns
    diagnostics["missing_normalized_columns"] = missing_normalized_columns

    if set(REQUIRED_POSITION_COLUMNS).issubset(df.columns):
        diagnostics["valid_coordinates"] = int(df[["latitude", "longitude"]].notna().all(axis=1).sum())

    if "timestamp" in df.columns:
        diagnostics["valid_timestamps"] = int(pd.to_datetime(df["timestamp"], errors="coerce", utc=True).notna().sum())

    if "state" in df.columns:
        diagnostics["states"] = sorted(str(s) for s in df["state"].dropna().unique())

    diagnostics["data_quality"] = {
        "rows": int(len(df)),
        "valid_coordinates": int(diagnostics["valid_coordinates"]),
        "valid_timestamps": int(diagnostics["valid_timestamps"]),
        "warnings_count": int(len(result.warnings)),
    }

    return diagnostics


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.kml and not args.csv:
        parser.error("Provide at least --kml or --csv.")

    result = run_pipeline(
        kml_path=args.kml,
        csv_path=args.csv,
        field_data_path=args.field_data,
        area_ha=args.area_ha,
        output_path=args.output,
    )

    payload = {"metrics": result.metrics, "warnings": result.warnings, "report": str(result.report_path)}
    if args.diagnose:
        payload["diagnostics"] = build_diagnostics(result, args)

    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
