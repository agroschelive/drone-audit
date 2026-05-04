import json
import pandas as pd
from drone_audit.cli import main


def test_cli_accepts_xlsx(tmp_path, capsys, monkeypatch):
    monkeypatch.setattr(pd, 'read_excel', lambda *a, **k: pd.DataFrame({'Data Hora':['2026-01-01T00:00:00Z'],'Área':[2.0]}))
    x = tmp_path/'input.xlsx'
    x.write_text('stub', encoding='utf-8')
    out = tmp_path/'r.html'
    rc = main(['--xlsx', str(x), '--output', str(out), '--diagnose', '--operation-name', 'Op1'])
    assert rc == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload['metrics']['operation_name'] == 'Op1'
