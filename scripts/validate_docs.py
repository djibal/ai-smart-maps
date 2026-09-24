from pathlib import Path

required = [
    "docs/index.md",
    "docs/vision/objectives.md",
    "docs/architecture/logical.md",
    "docs/architecture/decisions/index.md",
    "docs/risks/register.md",
    "docs/phases/index.md",
    "docs/_state/ledger.md",
]

for f in required:
    assert Path(f).exists(), f"missing {f}"

for p in Path("docs").rglob("*.md"):
    text = p.read_text(encoding="utf-8")
    assert "\ufffd" not in text, f"replacement char in {p}"

print("docs ok")
