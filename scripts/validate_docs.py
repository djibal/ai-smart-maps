from pathlib import Path

required = [
    "docs/index.md",
    "docs/vision/objectives.md",
    "docs/vision/constraints.md",
    "docs/architecture/logical.md",
    "docs/architecture/tradeoffs.md",
    "docs/architecture/decisions/index.md",
    "docs/risks/assumptions.md",
    "docs/risks/register.md",
    "docs/roadmap/phases.md",
    "docs/experiments/index.md",
    "docs/experiments/A1-report.md",
    "docs/experiments/A2-report.md",
    "docs/experiments/A3-report.md",
    "docs/experiments/A6-report.md",
    "docs/experiments/FARAL-report.md",
    "docs/experiments/TDLA-report.md",
    "docs/experiments/A4-report.md",
    "docs/experiments/A4-v2-report.md",
    "docs/experiments/A4-v3-report.md",
    "docs/_state/ledger.md",
]

for f in required:
    assert Path(f).exists(), f"missing {f}"

for p in Path("docs").rglob("*.md"):
    text = p.read_text(encoding="utf-8")
    assert "\ufffd" not in text, f"replacement char in {p}"

print("docs ok")
