from __future__ import annotations

import argparse
import json
from pathlib import Path

from drone_audit.pipeline import run_pipeline


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate a simple auxiliary report from exported operation files.")
    parser.add_argument("--kml", type=Path, help="Path to a KML file.")
    parser.add_argument("--csv", type=Path, help="Path to a CSV file.")
    parser.add_argument("--field-data", type=Path, help="Optional JSON with complementary field data.")
    parser.add_argument("--area-ha", type=float, help="Optional operated area in hectares.")
    parser.add_argument("--output", type=Path, default=Path("reports/drone_audit_report.html"), help="Output HTML report path.")
    return parser


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

    print(json.dumps({"metrics": result.metrics, "warnings": result.warnings, "report": str(result.report_path)}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
