from pathlib import Path
import ftfy

for p in Path("docs").rglob("*.md"):
    raw = p.read_text(encoding="utf-8", errors="replace")
    fixed = ftfy.fix_text(raw)
    if fixed != raw:
        p.write_text(fixed, encoding="utf-8")
        print(f"fixed {p}")
