from __future__ import annotations

import argparse
import json
from pathlib import Path

from drone_audit.pipeline import PipelineResult, run_pipeline


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Generate a simple auxiliary report from exported operation files.")
    p.add_argument("--kml", type=Path)
    p.add_argument("--csv", type=Path)
    p.add_argument("--xlsx", type=Path)
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
    return {
        "rows": int(len(result.dataframe)),
        "columns": [str(c) for c in result.dataframe.columns],
        "recognized_inputs": {"kml": bool(args.kml), "csv": bool(args.csv), "xlsx": bool(args.xlsx), "field_data": bool(args.field_data)},
        "data_quality": result.metrics.get("data_quality", []),
        "source": result.metrics.get("data_source"),
    }


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if not args.kml and not args.csv and not args.xlsx:
        raise SystemExit("Provide at least --kml, --csv or --xlsx.")
    result = run_pipeline(kml_path=args.kml, csv_path=args.csv, xlsx_path=args.xlsx, field_data_path=args.field_data,
                          area_ha=args.area_ha, output_path=args.output, import_index_path=args.import_index,
                          dedupe=not args.no_dedupe, operation_name=args.operation_name, drone_model=args.drone_model,
                          operator=args.operator, farm_name=args.farm_name, field_name=args.field_name)
    payload = {"metrics": result.metrics, "warnings": result.warnings, "report": str(result.report_path)}
    if args.diagnose:
        payload["diagnostics"] = build_diagnostics(result, args)
    print(json.dumps(payload, indent=2, ensure_ascii=False, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
