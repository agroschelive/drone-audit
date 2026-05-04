from __future__ import annotations

from pathlib import Path
import io
import pandas as pd
from drone_audit.parsers.base import ParsedData
from drone_audit.telemetry_normalizer import normalize_telemetry_dataframe

ERR = "Arquivo TXT não parece ser um log tabular legível. Logs DJI criptografados ainda não são suportados diretamente."


def _binary_like(raw: bytes) -> bool:
    if not raw:
        return True
    sample = raw[:8192]
    bad = sum(1 for b in sample if b == 0 or (b < 9) or (13 < b < 32))
    return bad / max(1, len(sample)) > 0.15


def parse_txt(path):
    p = Path(path)
    raw = p.read_bytes()
    if _binary_like(raw):
        return ParsedData(pd.DataFrame(), ["txt_nao_tabular", ERR], "txt")
    text = raw.decode("utf-8", errors="replace")
    seps = [",", ";", "\t", "|", r"\s+"]
    for sep in seps:
        try:
            df = pd.read_csv(io.StringIO(text), sep=sep, engine="python")
            if df.shape[1] < 2:
                continue
            if any(str(c).startswith("Unnamed") for c in df.columns):
                continue
            ndf, w = normalize_telemetry_dataframe(df, "txt")
            return ParsedData(ndf, w, "txt")
        except Exception:
            continue
    return ParsedData(pd.DataFrame(), ["txt_nao_tabular", ERR], "txt")
