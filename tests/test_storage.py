from drone_audit.storage import file_sha256, load_import_index, register_import, save_import_index, is_duplicate_file


def test_storage_index(tmp_path):
    f = tmp_path/'a.txt'
    f.write_text('abc', encoding='utf-8')
    h = file_sha256(f)
    idx = load_import_index(tmp_path/'idx.json')
    assert not is_duplicate_file(h, idx)
    idx = register_import(h, {'name':'a'}, idx)
    save_import_index(tmp_path/'idx.json', idx)
    idx2 = load_import_index(tmp_path/'idx.json')
    assert is_duplicate_file(h, idx2)
