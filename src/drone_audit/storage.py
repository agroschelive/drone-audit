from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_IMPORT_INDEX = Path(".drone_audit/import_index.json")


def file_sha256(path: str | Path) -> str:
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def load_import_index(index_path: str | Path) -> dict:
    p = Path(index_path)
    if not p.exists():
        return {"imports": {}}
    return json.loads(p.read_text(encoding="utf-8"))


def save_import_index(index_path: str | Path, data: dict) -> None:
    p = Path(index_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def is_duplicate_file(file_hash: str, index: dict) -> bool:
    return file_hash in index.get("imports", {})


def register_import(file_hash: str, metadata: dict, index: dict) -> dict:
    imported_at = datetime.now(timezone.utc).isoformat()  # noqa: UP017
    index.setdefault("imports", {})[file_hash] = {**metadata, "imported_at": imported_at}
    return index
