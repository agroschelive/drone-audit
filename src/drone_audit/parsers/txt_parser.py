from __future__ import annotations

from pathlib import Path
import pandas as pd

from drone_audit.parsers.base import ParsedData
from drone_audit.telemetry_normalizer import normalize_telemetry_dataframe

ERR = "Arquivo TXT não parece ser um log tabular legível. Logs DJI criptografados ainda não são suportados diretamente."

def parse_txt(path):
    p=Path(path)
    raw=p.read_bytes()
    if b"\x00" in raw[:4096]:
        return ParsedData(dataframe=pd.DataFrame(), warnings=["txt_nao_tabular", ERR], source_type="txt")
    text=raw.decode("utf-8", errors="replace")
    if not any(sep in text for sep in [",",";","\t"," "]):
        return ParsedData(dataframe=pd.DataFrame(), warnings=["txt_nao_tabular", ERR], source_type="txt")
    df=pd.read_csv(p, sep=None, engine="python")
    ndf,w=normalize_telemetry_dataframe(df,"txt")
    return ParsedData(dataframe=ndf,warnings=w,source_type="txt")
