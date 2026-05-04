from pathlib import Path


def test_required_governance_docs_exist():
    for path in [
        'docs/support-matrix.md',
        'docs/local-real-file-validation.md',
        'docs/release-checklist.md',
        'docs/sanitization.md',
        'docs/quality-gates.md',
        'examples/real_samples/README.md',
        'SECURITY.md',
        'CONTRIBUTING.md',
    ]:
        assert Path(path).exists(), f'missing: {path}'


def test_readme_links_core_docs():
    text = Path('README.md').read_text(encoding='utf-8').lower()
    for ref in [
        'docs/support-matrix.md',
        'docs/local-real-file-validation.md',
        'docs/release-checklist.md',
        'docs/sanitization.md',
        'docs/quality-gates.md',
    ]:
        assert ref in text


def test_support_matrix_explicit_limits():
    text = Path('docs/support-matrix.md').read_text(encoding='utf-8').lower()
    assert 'dat' in text and 'not implemented' in text
    assert 'txt bruto dji' in text and 'not implemented' in text


def test_sanitization_anonymity_warning():
    text = Path('docs/sanitization.md').read_text(encoding='utf-8').lower()
    assert 'does not automatically guarantee anonymity' in text


def test_local_real_files_must_stay_local():
    text = Path('docs/local-real-file-validation.md').read_text(encoding='utf-8').lower()
    assert 'keep real files local only' in text


def test_github_templates_exist_and_warn_privacy():
    paths = [
        '.github/ISSUE_TEMPLATE/bug_report.md',
        '.github/ISSUE_TEMPLATE/feature_request.md',
        '.github/ISSUE_TEMPLATE/data_format_validation.md',
        '.github/pull_request_template.md',
    ]
    for p in paths:
        assert Path(p).exists(), f'missing: {p}'

    joined = '\n'.join(Path(p).read_text(encoding='utf-8').lower() for p in paths)
    assert 'do not attach raw real drone files' in joined
    assert 'real coordinates' in joined
    assert 'client names' in joined
    assert 'property names' in joined
    assert 'serial numbers' in joined


def test_no_real_raw_samples_inside_real_samples_folder():
    root = Path('examples/real_samples')
    assert root.exists()
    disallowed = {'.dat', '.txt', '.csv', '.kml', '.xlsx', '.xls'}
    for item in root.rglob('*'):
        if item.is_file() and item.name.lower() != 'readme.md':
            assert item.suffix.lower() not in disallowed, f'raw sample found: {item}'
