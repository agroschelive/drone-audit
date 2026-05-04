from pathlib import Path

from drone_audit.schema import NORMALIZED_COLUMNS


def test_readme_mentions_diagnose_and_modern_install():
    readme = Path("README.md").read_text(encoding="utf-8")
    assert "pip install -r requirements.txt" not in readme
    assert "pip install -e ." in readme
    assert "--diagnose" in readme


def test_development_docs_exist_and_have_expected_content():
    architecture = Path("docs/architecture.md")
    development = Path("docs/development.md")
    assert architecture.exists()
    assert development.exists()
    assert "normalized schema" in architecture.read_text(encoding="utf-8").lower()
    assert "ruff check" in development.read_text(encoding="utf-8").lower()


def test_schema_contains_expected_columns():
    expected = {
        "timestamp",
        "latitude",
        "longitude",
        "speed_m_s",
        "valve_open",
        "battery_pct",
        "source",
        "state",
    }
    assert expected.issubset(set(NORMALIZED_COLUMNS))


def test_ci_and_pyproject_include_tooling():
    pyproject = Path("pyproject.toml").read_text(encoding="utf-8")
    ci = Path(".github/workflows/ci.yml").read_text(encoding="utf-8")
    assert "[tool.ruff]" in pyproject
    assert "dev =" in pyproject
    assert "ruff check" in ci
    assert "--cov=drone_audit" in ci


def test_standalone_prototype_removed_and_roadmap_governance_guardrails():
    assert not Path("drone_audit_pipeline.py").exists()

    roadmap_path = Path("docs/roadmap-backlog.md")
    assert roadmap_path.exists()
    text = roadmap_path.read_text(encoding="utf-8")
    lower = text.lower()

    assert "# roadmap backlog" in lower
    assert "roadmap de issues" not in lower
    assert "curto prazo" not in lower
    assert "médio prazo" not in lower
    assert "longo prazo" not in lower
    assert "arquivos originais" not in lower

    assert "locally" in lower
    assert "must not be committed" in lower

    assert "implement dat" not in lower
    assert "dat support already exists" not in lower
    assert "research dat support" in lower
    assert "before any implementation" in lower
