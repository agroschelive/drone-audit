from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import xml.etree.ElementTree as ET

import pandas as pd


@dataclass(frozen=True)
class ParsedKML:
    dataframe: pd.DataFrame
    warnings: list[str]


def _safe_text(value: str | None) -> str:
    return (value or "").strip()


def _parse_float(value: str) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _parse_kml_coordinates_text(text: str) -> list[tuple[float, float, float | None]]:
    points: list[tuple[float, float, float | None]] = []
    for item in text.replace("\n", " ").replace("\t", " ").split():
        parts = item.split(",")
        if len(parts) < 2:
            continue
        lon = _parse_float(parts[0])
        lat = _parse_float(parts[1])
        alt = _parse_float(parts[2]) if len(parts) >= 3 and parts[2] != "" else None
        if lat is None or lon is None:
            continue
        points.append((lat, lon, alt))
    return points


def _parse_gx_coord_text(text: str | None) -> tuple[float, float, float | None] | None:
    parts = _safe_text(text).split()
    if len(parts) < 2:
        return None
    lon = _parse_float(parts[0])
    lat = _parse_float(parts[1])
    alt = _parse_float(parts[2]) if len(parts) >= 3 else None
    if lat is None or lon is None:
        return None
    return lat, lon, alt


def parse_kml(path: str | Path) -> ParsedKML:
    """Parse a minimal KML route into a normalized dataframe.

    Supports common KML LineString coordinates and gx:Track coordinates.
    The parser is intentionally small and does not try to understand every KML extension.
    """
    kml_path = Path(path)
    warnings: list[str] = []

    raw = kml_path.read_text(encoding="utf-8-sig", errors="ignore")
    try:
        root = ET.fromstring(raw)
    except ET.ParseError as exc:
        raise ValueError(f"Invalid KML file: {kml_path}") from exc

    rows: list[dict] = []
    segment_id = 0

    for track in root.findall(".//{*}Track"):
        segment_id += 1
        when_nodes = track.findall("{*}when")
        coord_nodes = track.findall("{*}coord")
        timestamps = [
            pd.to_datetime(_safe_text(node.text), errors="coerce", utc=True)
            for node in when_nodes
        ]
        coords = [_parse_gx_coord_text(node.text) for node in coord_nodes]
        coords = [coord for coord in coords if coord is not None]

        if timestamps and len(timestamps) != len(coords):
            warnings.append("gx:Track has a different number of timestamps and coordinates.")

        for idx, (lat, lon, alt) in enumerate(coords):
            rows.append(
                {
                    "timestamp": timestamps[idx] if idx < len(timestamps) else pd.NaT,
                    "latitude": lat,
                    "longitude": lon,
                    "altitude_m": alt,
                    "segment_id": segment_id,
                    "source": "kml:gxtrack",
                }
            )

    for linestring in root.findall(".//{*}LineString"):
        for coord_node in linestring.findall("{*}coordinates"):
            coords = _parse_kml_coordinates_text(coord_node.text or "")
            if not coords:
                continue
            segment_id += 1
            for lat, lon, alt in coords:
                rows.append(
                    {
                        "timestamp": pd.NaT,
                        "latitude": lat,
                        "longitude": lon,
                        "altitude_m": alt,
                        "segment_id": segment_id,
                        "source": "kml:linestring",
                    }
                )

    if not rows:
        warnings.append("No route coordinates found in KML.")

    return ParsedKML(dataframe=pd.DataFrame(rows), warnings=warnings)
