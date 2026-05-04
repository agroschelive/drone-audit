from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path

import pandas as pd


@dataclass(frozen=True)
class TelemetryPoint:
    timestamp: str
    latitude: float | None
    longitude: float | None
    altitude: float | None = None
    speed: float | None = None
    battery_percentual: float | None = None
    vazao: float | None = None
    valve_open: bool | None = None


def parse_telemetry_file(path: str | Path) -> list[TelemetryPoint]:
    input_path = Path(path)
    if input_path.suffix.lower() == ".json":
        items = json.loads(input_path.read_text(encoding="utf-8"))
        return [TelemetryPoint(**item) for item in items]

    df = pd.read_csv(input_path)
    rows: list[TelemetryPoint] = []
    for row in df.to_dict(orient="records"):
        rows.append(
            TelemetryPoint(
                timestamp=str(row.get("timestamp")),
                latitude=row.get("latitude"),
                longitude=row.get("longitude"),
                altitude=row.get("altitude"),
                speed=row.get("speed") or row.get("speed_m_s"),
                battery_percentual=row.get("battery_percentual") or row.get("battery_pct"),
                vazao=row.get("vazao"),
                valve_open=row.get("valve_open"),
            )
        )
    return rows


def telemetry_to_eventos_voo(points: list[TelemetryPoint], voo_id: str) -> list[dict]:
    if len(points) < 2:
        return []
    eventos: list[dict] = []
    ts = pd.to_datetime([p.timestamp for p in points], utc=True, errors="coerce")

    for i in range(len(points) - 1):
        point = points[i]
        start = ts[i]
        end = ts[i + 1]
        duracao = max(0, int((end - start).total_seconds())) if pd.notna(start) and pd.notna(end) else 0
        speed = float(point.speed or 0.0)
        valve_open = bool(point.valve_open)

        if valve_open and speed >= 0.8:
            tipo = "pulverizando"
        elif speed >= 1.0:
            tipo = "deslocando"
        else:
            tipo = "parado"

        evento = {
            "voo_id": voo_id,
            "tipo_evento": tipo,
            "inicio": start.isoformat() if pd.notna(start) else None,
            "fim": end.isoformat() if pd.notna(end) else None,
            "duracao_segundos": duracao,
            "latitude": point.latitude,
            "longitude": point.longitude,
            "velocidade": point.speed,
            "altitude": point.altitude,
            "bateria_percentual": point.battery_percentual,
            "vazao": point.vazao,
            "volume_aplicado": (float(point.vazao or 0) * duracao) / 60.0,
            "criado_em": pd.Timestamp.utcnow().isoformat(),
        }
        eventos.append(evento)
    return eventos
