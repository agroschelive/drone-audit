from __future__ import annotations
from pathlib import Path
import xml.etree.ElementTree as ET
from drone_audit.agras.types.agras_models import AgrasTelemetryPoint

def parse_smartfarm_kml(path: str | Path) -> list[AgrasTelemetryPoint]:
    root = ET.fromstring(Path(path).read_text(encoding="utf-8-sig", errors="ignore"))
    pts: list[AgrasTelemetryPoint] = []
    seq = 0
    for tr in root.findall('.//{*}Track'):
        whens = [w.text for w in tr.findall('{*}when')]
        coords = [c.text for c in tr.findall('{*}coord')]
        for i, c in enumerate(coords):
            if not c:
                continue
            parts = c.strip().split()
            if len(parts) < 2:
                continue
            seq += 1
            pts.append(AgrasTelemetryPoint(latitude=float(parts[1]), longitude=float(parts[0]), altitude_m=float(parts[2]) if len(parts)>2 else None, sequencia=seq, timestamp=None, fonte="smartfarm_kml"))
    for ls in root.findall('.//{*}LineString'):
        for cn in ls.findall('{*}coordinates'):
            for c in (cn.text or '').replace('\n',' ').split():
                p = c.split(',')
                if len(p)<2: continue
                seq += 1
                pts.append(AgrasTelemetryPoint(latitude=float(p[1]), longitude=float(p[0]), altitude_m=float(p[2]) if len(p)>2 and p[2] else None, sequencia=seq, timestamp=None, fonte="smartfarm_kml"))
    return pts
