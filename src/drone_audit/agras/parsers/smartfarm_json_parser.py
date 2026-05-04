from __future__ import annotations

import json
from pathlib import Path

from drone_audit.agras.types.agras_models import AgrasRawSmartFarmRow


def parse_smartfarm_json(path: str | Path) -> list[AgrasRawSmartFarmRow]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    rows: list[AgrasRawSmartFarmRow] = []

    if isinstance(data, list):
        for i, item in enumerate(data, start=1):
            if isinstance(item, dict):
                rows.append(AgrasRawSmartFarmRow(source_row=i, values=item))
    elif isinstance(data, dict):
        flights = data.get("flights") or data.get("operation", {}).get("flights") or []
        for i, item in enumerate(flights, start=1):
            if isinstance(item, dict):
                rows.append(AgrasRawSmartFarmRow(source_row=i, values=item))

    return rows
