from __future__ import annotations

from html import escape
from pathlib import Path
from typing import Any

import pandas as pd

try:
    import folium
except Exception:  # pragma: no cover
    folium = None


def _format_number(value: Any, digits: int = 2) -> str:
    if value is None:
        return "not available"
    try:
        return f"{float(value):.{digits}f}"
    except (TypeError, ValueError):
        return escape(str(value))


def _map_html(df: pd.DataFrame) -> str:
    if folium is None or df.empty or {"latitude", "longitude"} - set(df.columns):
        return "<p>Map not available for these data.</p>"

    coords_df = df[["latitude", "longitude"]].dropna()
    if coords_df.empty:
        return "<p>Map not available for these data.</p>"

    coords = [(float(row.latitude), float(row.longitude)) for row in coords_df.itertuples()]
    fmap = folium.Map(location=coords[0], zoom_start=16, control_scale=True)
    if len(coords) >= 2:
        folium.PolyLine(locations=coords, weight=4, tooltip="Route").add_to(fmap)
    folium.Marker(location=coords[0], tooltip="Start").add_to(fmap)
    folium.Marker(location=coords[-1], tooltip="End").add_to(fmap)
    return fmap._repr_html_()


def build_html_report(
    df: pd.DataFrame,
    metrics: dict[str, Any],
    field_data: dict[str, Any] | None = None,
) -> str:
    field_data = field_data or {}
    state_durations = metrics.get("state_durations_s") or {}
    state_rows = "".join(
        f"<tr><td>{escape(str(state))}</td><td>{_format_number(seconds, 1)} s</td></tr>"
        for state, seconds in state_durations.items()
    ) or "<tr><td colspan='2'>not available</td></tr>"

    field_rows = "".join(
        f"<tr><td>{escape(str(key))}</td><td>{escape(str(value))}</td></tr>"
        for key, value in field_data.items()
    ) or "<tr><td colspan='2'>not provided</td></tr>"

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Drone Audit - Auxiliary Report</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 32px; color: #222; }}
    h1, h2 {{ color: #113322; }}
    .warning {{ background: #fff8d8; padding: 12px; border: 1px solid #e8d26a; }}
    table {{ border-collapse: collapse; width: 100%; margin: 12px 0; }}
    th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
    th {{ background: #f2f2f2; }}
  </style>
</head>
<body>
  <h1>Drone Audit - Auxiliary Report</h1>
  <div class="warning">
    This report is auxiliary and experimental. It does not replace professional interpretation, field validation or technical responsibility.
  </div>

  <h2>Summary</h2>
  <table>
    <tr><th>Metric</th><th>Value</th></tr>
    <tr><td>Analyzed points</td><td>{len(df)}</td></tr>
    <tr><td>Traveled distance</td><td>{_format_number(metrics.get('distance_m'))} m</td></tr>
    <tr><td>Total time</td><td>{_format_number(metrics.get('time_s'), 1)} s</td></tr>
    <tr><td>Provided area</td><td>{_format_number(metrics.get('area_ha'))} ha</td></tr>
    <tr><td>Estimated productivity</td><td>{_format_number(metrics.get('productivity_ha_h'))} ha/h</td></tr>
  </table>

  <h2>Estimated states</h2>
  <table>
    <tr><th>State</th><th>Duration</th></tr>
    {state_rows}
  </table>

  <h2>Complementary data</h2>
  <table>
    <tr><th>Field</th><th>Value</th></tr>
    {field_rows}
  </table>

  <h2>Map</h2>
  {_map_html(df)}
</body>
</html>
"""


def write_html_report(path: str | Path, html: str) -> Path:
    out_path = Path(path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")
    return out_path
