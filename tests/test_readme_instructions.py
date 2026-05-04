from pathlib import Path


def test_readme_does_not_reference_requirements_txt():
    readme = Path("README.md").read_text(encoding="utf-8")
    assert "pip install -r requirements.txt" not in readme


def test_readme_references_editable_install():
    readme = Path("README.md").read_text(encoding="utf-8")
    assert "pip install -e ." in readme
    assert "pip install -e \".[dev]\"" in readme
