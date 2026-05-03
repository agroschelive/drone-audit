from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_field_data(path: str | Path | None) -> dict[str, Any]:
    if path is None:
        return {}
    field_path = Path(path)
    with field_path.open("r", encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, dict):
        raise ValueError("Field data JSON must be an object.")
    return data
