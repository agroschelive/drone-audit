from drone_audit.field_aliases import map_columns

def test_aliases():
    m=map_columns(["Spray_Status","flow_rate","largura_faixa"])
    assert m["spray_on"]=="Spray_Status"
    assert m["flow_l_min"]=="flow_rate"
    assert m["swath_width_m"]=="largura_faixa"
