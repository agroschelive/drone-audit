from __future__ import annotations

from pathlib import Path

import pandas as pd

from drone_audit.agras.parsers.smartfarm_csv_parser import ALIASES, _norm
from drone_audit.agras.types.agras_models import AgrasImportPreview, AgrasRawSmartFarmRow


def parse_smartfarm_xlsx(path: str | Path, sheet: int | str = 0) -> AgrasImportPreview:
    df = pd.read_excel(path, sheet_name=sheet)
    df = df.rename(columns={c: ALIASES.get(_norm(str(c)), _norm(str(c))) for c in df.columns})

    valid: list[AgrasRawSmartFarmRow] = []
    invalid: list[dict[str, str | int]] = []

    for i, row in df.iterrows():
        values = {k: (None if pd.isna(v) else v) for k, v in row.to_dict().items()}
        if not any(v is not None and str(v).strip() != "" for v in values.values()):
            invalid.append({"row": int(i) + 2, "error": "linha vazia"})
            continue
        valid.append(AgrasRawSmartFarmRow(source_row=int(i) + 2, values=values))

    return AgrasImportPreview(valid_rows=valid, invalid_rows=invalid, warnings=[])
