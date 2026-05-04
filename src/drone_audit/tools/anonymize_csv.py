from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from drone_audit.privacy import sanitize_csv_dataframe


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Sanitize CSV exports for public sharing.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--fake-coordinates", action="store_true")
    parser.add_argument("--no-normalize-timestamps", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    input_path = Path(args.input)
    output_path = Path(args.output)

    df = pd.read_csv(input_path)
    sanitized = sanitize_csv_dataframe(
        df,
        remove_coordinates=True,
        fake_coordinates=args.fake_coordinates,
        normalize_timestamps=not args.no_normalize_timestamps,
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    sanitized.to_csv(output_path, index=False)

    summary = {
        "input": str(input_path),
        "output": str(output_path),
        "rows": len(sanitized),
        "columns_before": list(df.columns),
        "columns_after": list(sanitized.columns),
        "coordinates_removed": "latitude" not in sanitized.columns and "longitude" not in sanitized.columns,
        "fake_coordinates": args.fake_coordinates,
        "timestamps_normalized": not args.no_normalize_timestamps,
    }
    print(json.dumps(summary))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
