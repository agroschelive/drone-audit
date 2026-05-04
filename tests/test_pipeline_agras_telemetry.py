from drone_audit.pipeline import run_pipeline


def test_pipeline_txt(tmp_path):
    p = tmp_path / "a.txt"
    p.write_text("time,lat,lon,flow\n2026-01-01,1,2,1\n")
    out = tmp_path / "r.html"
    run_pipeline(txt_path=p, output_path=out)
    assert out.exists()
