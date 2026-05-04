from __future__ import annotations
import csv
from pathlib import Path
from drone_audit.agras.types.agras_models import AgrasImportPreview, AgrasRawSmartFarmRow

ALIASES = {"date": "data", "start_time": "inicio", "end_time": "fim", "aircraft": "drone", "pilot": "operador", "hectares": "area_ha", "spray_area": "area_ha", "distance": "distancia", "volume": "volume"}

def _norm(s: str) -> str:
    return s.strip().lower().replace(" ", "_")

def parse_smartfarm_csv(path: str | Path) -> AgrasImportPreview:
    text = Path(path).read_text(encoding="utf-8", errors="replace")
    sample = text[:2048]
    dialect = csv.Sniffer().sniff(sample, delimiters=",;\t")
    rows = list(csv.DictReader(text.splitlines(), dialect=dialect))
    valid: list[AgrasRawSmartFarmRow] = []
    invalid: list[dict] = []
    for idx, row in enumerate(rows, start=2):
        out = {}
        for k, v in row.items():
            nk = _norm(k)
            out[ALIASES.get(nk, nk)] = v
        if not any(out.values()):
            invalid.append({"row": idx, "error": "linha vazia"})
            continue
        valid.append(AgrasRawSmartFarmRow(source_row=idx, values=out))
    return AgrasImportPreview(valid_rows=valid, invalid_rows=invalid, warnings=[])
