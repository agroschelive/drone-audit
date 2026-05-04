from __future__ import annotations

from pathlib import Path
import xml.etree.ElementTree as ET

from drone_audit.agras.types.agras_models import AgrasTelemetryPoint


def parse_smartfarm_kml(path: str | Path) -> list[AgrasTelemetryPoint]:
    root = ET.fromstring(Path(path).read_text(encoding="utf-8-sig", errors="ignore"))
    points: list[AgrasTelemetryPoint] = []
    sequence = 0

    for track in root.findall(".//{*}Track"):
        coords = [coord.text for coord in track.findall("{*}coord")]
        for coord_text in coords:
            if not coord_text:
                continue
            parts = coord_text.strip().split()
            if len(parts) < 2:
                continue
            sequence += 1
            points.append(
                AgrasTelemetryPoint(
                    latitude=float(parts[1]),
                    longitude=float(parts[0]),
                    altitude_m=float(parts[2]) if len(parts) > 2 else None,
                    sequencia=sequence,
                    timestamp=None,
                    fonte="smartfarm_kml",
                )
            )

    for line_string in root.findall(".//{*}LineString"):
        for coord_node in line_string.findall("{*}coordinates"):
            for coord_text in (coord_node.text or "").replace("\n", " ").split():
                parts = coord_text.split(",")
                if len(parts) < 2:
                    continue
                sequence += 1
                points.append(
                    AgrasTelemetryPoint(
                        latitude=float(parts[1]),
                        longitude=float(parts[0]),
                        altitude_m=float(parts[2]) if len(parts) > 2 and parts[2] else None,
                        sequencia=sequence,
                        timestamp=None,
                        fonte="smartfarm_kml",
                    )
                )

    return points
