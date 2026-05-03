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
        return "não disponível"
    try:
        return f"{float(value):.{digits}f}"
    except (TypeError, ValueError):
        return escape(str(value))


def _map_html(df: pd.DataFrame) -> str:
    if folium is None or df.empty or {"latitude", "longitude"} - set(df.columns):
        return "<p>Mapa não disponível para estes dados.</p>"

    coords_df = df[["latitude", "longitude"]].dropna()
    if coords_df.empty:
        return "<p>Mapa não disponível para estes dados.</p>"

    coords = [(float(row.latitude), float(row.longitude)) for row in coords_df.itertuples()]
    fmap = folium.Map(location=coords[0], zoom_start=16, control_scale=True)
    if len(coords) >= 2:
        folium.PolyLine(locations=coords, weight=4, tooltip="Rota").add_to(fmap)
    folium.Marker(location=coords[0], tooltip="Início").add_to(fmap)
    folium.Marker(location=coords[-1], tooltip="Fim").add_to(fmap)
    return fmap._repr_html_()


def build_html_report(
    df: pd.DataFrame,
    metrics: dict[str, Any],
    field_data: dict[str, Any] | None = None,
    warnings: list[str] | None = None,
) -> str:
    field_data = field_data or {}
    warnings = warnings or []
    state_durations = metrics.get("state_durations_s") or {}
    state_rows = "".join(
        f"<tr><td>{escape(str(state))}</td><td>{_format_number(seconds, 1)} s</td></tr>"
        for state, seconds in state_durations.items()
    ) or "<tr><td colspan='2'>não disponível</td></tr>"

    field_rows = "".join(
        f"<tr><td>{escape(str(key))}</td><td>{escape(str(value))}</td></tr>"
        for key, value in field_data.items()
    ) or "<tr><td colspan='2'>não informado</td></tr>"

    warning_items = "".join(
        f"<li>{escape(str(message))}</li>"
        for message in warnings
    )
    warning_list = f"<ul>{warning_items}</ul>" if warning_items else "<p>Nenhum aviso de processamento.</p>"

    return f"""<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <title>Drone Audit - Relatório Auxiliar</title>
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
  <h1>Drone Audit - Relatório Auxiliar</h1>
  <div class="warning">
    Este relatório é auxiliar e experimental. Não substitui interpretação profissional, validação em campo ou responsabilidade técnica.
  </div>

  <h2>Resumo</h2>
  <table>
    <tr><th>Métrica</th><th>Valor</th></tr>
    <tr><td>Pontos analisados</td><td>{len(df)}</td></tr>
    <tr><td>Distância percorrida</td><td>{_format_number(metrics.get('distance_m'))} m</td></tr>
    <tr><td>Tempo total</td><td>{_format_number(metrics.get('time_s'), 1)} s</td></tr>
    <tr><td>Área informada</td><td>{_format_number(metrics.get('area_ha'))} ha</td></tr>
    <tr><td>Produtividade estimada</td><td>{_format_number(metrics.get('productivity_ha_h'))} ha/h</td></tr>
  </table>

  <h2>Estados estimados</h2>
  <table>
    <tr><th>Estado</th><th>Duração</th></tr>
    {state_rows}
  </table>

  <h2>Avisos de processamento</h2>
  {warning_list}

  <h2>Dados complementares</h2>
  <table>
    <tr><th>Campo</th><th>Valor</th></tr>
    {field_rows}
  </table>

  <h2>Mapa</h2>
  {_map_html(df)}
</body>
</html>
"""


def write_html_report(path: str | Path, html: str) -> Path:
    out_path = Path(path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")
    return out_path
