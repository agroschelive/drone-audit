from drone_audit.pipeline import run_pipeline

def test_pipeline_agras_example(tmp_path):
    out=tmp_path/'r.html'
    res=run_pipeline(csv_path='examples/sample_agras_telemetry.csv', area_ha=1.5, planned_rate_l_ha=20, output_path=out)
    assert out.exists()
    assert res.metrics.get('spray_time_s') is not None
    assert res.metrics.get('volume_aplicado_l') is not None
    assert res.metrics.get('applied_area_ha') is not None
    assert res.metrics.get('real_rate_l_ha') is not None
    assert isinstance(res.metrics.get('diagnostics_auto'), list)
