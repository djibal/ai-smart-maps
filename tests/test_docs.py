from pathlib import Path

def test_required_docs():
    assert Path("docs/index.md").exists()
    assert Path("docs/_state/ledger.md").exists()
