import pandas as pd
from drone_audit.parsers.xlsx_parser import parse_xlsx


def test_parse_xlsx_basic(monkeypatch, tmp_path):
    sample = pd.DataFrame({'Data Hora Início':['2026-01-01 10:00:00'],'Data Hora Fim':['2026-01-01 10:10:00'],'Área':[5.2],'Volume':[60]})
    monkeypatch.setattr(pd, 'read_excel', lambda *a, **k: sample.copy())
    parsed = parse_xlsx(tmp_path/'sf.xlsx')
    assert parsed.source_type == 'xlsx_smartfarm'
    assert float(parsed.dataframe['area_ha'].iloc[0]) == 5.2
