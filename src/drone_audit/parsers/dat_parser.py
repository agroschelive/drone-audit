from __future__ import annotations

import pandas as pd
from drone_audit.parsers.base import ParsedData

MSG = "DAT bruto DJI/Agras ainda não é suportado. Converta localmente para CSV/TXT legível antes de importar."

def parse_dat(path):
    return ParsedData(dataframe=pd.DataFrame(), warnings=["dat_nao_suportado", MSG], source_type="dat")
