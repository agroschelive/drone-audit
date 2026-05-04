from drone_audit.parsers.dat_parser import parse_dat

def test_dat_stub():
    r=parse_dat('x.dat')
    assert 'dat_nao_suportado' in r.warnings
