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



def _metric_card(title: str, value: Any, unit: str = "") -> str:
    return f"<div class='card'><h3>{escape(title)}</h3><p>{_format_number(value)} {escape(unit)}</p></div>"

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

    op = metrics.get("operational") or {}

    source_info = metrics.get("data_source", "não informado")
    quality = metrics.get("data_quality", [])
    quality_html = "<ul>" + "".join(f"<li>{escape(str(w))}</li>" for w in quality) + "</ul>" if quality else "<p>sem avisos</p>"
    auto_diag = metrics.get("diagnostics_auto", [])
    auto_diag_html = "<ul>" + "".join(f"<li>{escape(str(a.get('code')))}: {escape(str(a.get('message')))}</li>" for a in auto_diag) + "</ul>" if auto_diag else "<p>não disponível</p>"
    op_alerts = metrics.get("operational_alerts") or []
    op_alert_items = "".join(f"<li>{escape(str(a))}</li>" for a in op_alerts)
    op_alert_list = f"<ul>{op_alert_items}</ul>" if op_alert_items else "<p>Sem alertas operacionais automáticos.</p>"

    cards = "".join([
        _metric_card("Área aplicada", metrics.get("effective_area_ha") or metrics.get("applied_area_ha") or metrics.get("area_ha"), "ha"),
        _metric_card("Tempo total", op.get("tempo_total_s"), "s"),
        _metric_card("Tempo pulverizando", op.get("tempo_pulverizando_s"), "s"),
        _metric_card("Tempo manobrando", op.get("tempo_manobrando_s"), "s"),
        _metric_card("Tempo parado", op.get("tempo_parado_s"), "s"),
        _metric_card("Eficiência operacional", op.get("eficiencia_operacional_pct"), "%"),
        _metric_card("Produtividade real", op.get("produtividade_real_ha_h"), "ha/h"),
        _metric_card("Consumo bateria/ha", op.get("consumo_bateria_ha_pct"), "%/ha"),
        _metric_card("Taxa real", op.get("taxa_real_l_ha"), "L/ha"),
    ])

    return f"""<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <title>Drone Audit - Relatório Auxiliar</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 32px; color: #222; }}
    h1, h2 {{ color: #113322; }}
    .warning {{ background: #fff8d8; padding: 12px; border: 1px solid #e8d26a; }}
    .cards {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(190px,1fr)); gap: 10px; margin-top: 10px; }}
    .card {{ border: 1px solid #ddd; border-radius: 8px; padding: 10px; background: #fafafa; }}
    .card h3 {{ font-size: 14px; margin: 0; color: #224; }}
    .card p {{ font-size: 18px; margin: 6px 0 0; }}
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

  <h2>Dashboard operacional</h2>
  <div class="cards">{cards}</div>

  <h2>Fonte principal dos dados</h2>
  <p><strong>Origem dos dados:</strong> {source_info}</p>
  <h2>Confiabilidade dos dados</h2>
  <p><strong>Qualidade dos dados:</strong>{quality_html}</p>
  <h2>Limitações da análise</h2><p>Análise auxiliar, experimental e estimada; não substitui responsável técnico.</p>
  <h2>Avisos técnicos</h2>{warning_list}
  <h2>Alertas operacionais</h2>{op_alert_list}
  <h2>Resumo</h2>
  <p><strong>Diagnóstico automático:</strong>{auto_diag_html}</p>
  <table>
    <tr><th>Métrica</th><th>Valor</th></tr>
    <tr><td>Pontos analisados</td><td>{len(df)}</td></tr>
    <tr><td>Distância percorrida</td><td>{_format_number(metrics.get('distance_m'))} m</td></tr>
    <tr><td>Tempo total</td><td>{_format_number(metrics.get('time_s'), 1)} s</td></tr>
    <tr><td>Área informada</td><td>{_format_number(metrics.get('area_ha'))} ha</td></tr>
    <tr><td>Área calculada</td><td>{_format_number(metrics.get('applied_area_ha'))} ha</td></tr>
    <tr><td>Área usada nos cálculos</td><td>{_format_number(metrics.get('effective_area_ha'))} ha</td></tr>
    <tr><td>Produtividade estimada</td><td>{_format_number(metrics.get('productivity_ha_h'))} ha/h</td></tr>
  </table>

  <h2>Estados estimados</h2>
  <table>
    <tr><th>Estado</th><th>Duração</th></tr>
    {state_rows}
  </table>

  <h2>Origem da área usada</h2><p>{escape(str(metrics.get("applied_area_ha"))) if metrics.get("applied_area_ha") is not None else "estimada/indisponível"}</p>
  <h2>Origem do volume usado</h2><p>{escape(str(metrics.get("volume_aplicado_l"))) if metrics.get("volume_aplicado_l") is not None else "estimada/indisponível"}</p>

  <h2>Diagnóstico automático</h2>
  {op_alert_list}

  <h2>Dados complementares</h2>
  <table>
    <tr><th>Campo</th><th>Valor</th></tr>
    {field_rows}
  </table>

  <h2>Relatório por missão</h2>
  <table>
    <tr><th>Campo</th><th>Valor</th></tr>
    <tr><td>Cliente</td><td>{escape(str(field_data.get("cliente", "não informado")))}</td></tr>
    <tr><td>Fazenda</td><td>{escape(str(field_data.get("fazenda", "não informado")))}</td></tr>
    <tr><td>Talhão</td><td>{escape(str(field_data.get("talhao", "não informado")))}</td></tr>
    <tr><td>Drone</td><td>{escape(str(field_data.get("drone", "não informado")))}</td></tr>
    <tr><td>Operador</td><td>{escape(str(field_data.get("operador", "não informado")))}</td></tr>
    <tr><td>Bateria</td><td>{escape(str(field_data.get("bateria", "não informado")))}</td></tr>
  </table>

  <h2>Tabela de eventos (estimada por estado)</h2>
  <table>
    <tr><th>Evento</th><th>Duração (s)</th></tr>
    {state_rows}
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
