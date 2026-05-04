from drone_audit.parsers.txt_parser import parse_txt

def test_txt_ok(tmp_path):
    p=tmp_path/'a.txt'; p.write_text('time,lat,lon\n2026-01-01,1,2\n')
    r=parse_txt(p)
    assert not r.dataframe.empty
