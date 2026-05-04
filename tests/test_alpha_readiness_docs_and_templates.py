from pathlib import Path


def test_new_docs_exist():
    for path in [
        'docs/support-matrix.md',
        'docs/local-real-file-validation.md',
        'docs/release-checklist.md',
        'docs/sanitization.md',
        'docs/quality-gates.md',
    ]:
        assert Path(path).exists()


def test_templates_exist():
    for path in [
        '.github/ISSUE_TEMPLATE/bug_report.md',
        '.github/ISSUE_TEMPLATE/feature_request.md',
        '.github/ISSUE_TEMPLATE/data_format_validation.md',
        '.github/pull_request_template.md',
    ]:
        assert Path(path).exists()


def test_readme_links_new_docs():
    readme = Path('README.md').read_text(encoding='utf-8').lower()
    assert 'docs/support-matrix.md' in readme
    assert 'docs/local-real-file-validation.md' in readme
    assert 'docs/release-checklist.md' in readme
    assert 'docs/sanitization.md' in readme
    assert 'docs/quality-gates.md' in readme


def test_support_matrix_guardrails():
    text = Path('docs/support-matrix.md').read_text(encoding='utf-8').lower()
    assert 'dat' in text and 'not implemented' in text
    assert 'txt/log exports' in text and 'not implemented' in text
    assert 'real files must remain local only' in text
    assert 'public examples must be synthetic or safely sanitized' in text


def test_local_validation_guardrails():
    text = Path('docs/local-real-file-validation.md').read_text(encoding='utf-8').lower()
    assert 'keep real files local only' in text
    assert 'do not commit raw real files' in text
    assert 'drone_audit.tools.anonymize_csv' in text
    assert 'dat/txt parsing is not implemented' in text


def test_release_checklist_guardrails():
    text = Path('docs/release-checklist.md').read_text(encoding='utf-8').lower()
    assert 'no real coordinates committed' in text
    assert 'no raw dat/txt/csv/kml real exports committed' in text
    assert 'ruff check src tests' in text
    assert 'pytest -q' in text


def test_sanitization_doc_guardrails():
    text = Path('docs/sanitization.md').read_text(encoding='utf-8').lower()
    assert 'does not automatically guarantee anonymity' in text
    assert 'must inspect sanitized output before publication' in text
    assert 'original_coordinates_removed' in text
    assert 'synthetic_coordinates_added' in text


def test_templates_privacy_warnings():
    bug = Path('.github/ISSUE_TEMPLATE/bug_report.md').read_text(encoding='utf-8').lower()
    feature = Path('.github/ISSUE_TEMPLATE/feature_request.md').read_text(encoding='utf-8').lower()
    validation = Path('.github/ISSUE_TEMPLATE/data_format_validation.md').read_text(encoding='utf-8').lower()
    pr = Path('.github/pull_request_template.md').read_text(encoding='utf-8').lower()

    for text in (bug, feature, validation):
        assert 'do not attach raw real drone files' in text
        assert 'real coordinates' in text

    assert 'no real files committed' in pr
    assert 'privacy/security impact considered' in pr


def test_existing_safety_roadmap_rules():
    assert not Path('drone_audit_pipeline.py').exists()
    roadmap = Path('docs/roadmap-backlog.md').read_text(encoding='utf-8').lower()
    assert '# roadmap backlog' in roadmap
    assert 'research dat support' in roadmap
    assert 'evaluate txt/log exports' in roadmap
