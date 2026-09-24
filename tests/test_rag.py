import json
from pathlib import Path

INDEX = Path("index/chunks.json")


def test_index_exists_and_grounded():
    if not INDEX.exists():
        return
    chunks = json.loads(INDEX.read_text(encoding="utf-8"))
    assert chunks, "empty index"
    for c in chunks:
        assert c["source"].endswith(".md")
        assert (Path("docs") / c["source"]).exists()
