from drone_audit.parsers.txt_parser import parse_txt


def test_parse_semicolon(tmp_path):
    p = tmp_path / "a.txt"
    p.write_text("time;lat;lon\n2026-01-01;1;2\n")
    r = parse_txt(p)
    assert not r.dataframe.empty


def test_parse_tab(tmp_path):
    p = tmp_path / "a.txt"
    p.write_text("time\tlat\tlon\n2026-01-01\t1\t2\n")
    r = parse_txt(p)
    assert not r.dataframe.empty


def test_reject_binary(tmp_path):
    p = tmp_path / "a.txt"
    p.write_bytes(b"\x00\x01\x02raw")
    r = parse_txt(p)
    assert "txt_nao_tabular" in r.warnings
