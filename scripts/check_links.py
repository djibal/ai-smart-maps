import re
from pathlib import Path

DOCS = Path("docs")
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")

def is_external(target: str) -> bool:
    return (
        target.startswith("http://")
        or target.startswith("https://")
        or target.startswith("mailto:")
        or target.startswith("#")
    )

errors = []
for md in DOCS.rglob("*.md"):
    text = md.read_text(encoding="utf-8")
    for target in LINK_RE.findall(text):
        target = target.split("#", 1)[0].strip()
        if not target or is_external(target):
            continue
        resolved = (md.parent / target).resolve()
        if not resolved.exists():
            errors.append(f"{md}: broken link -> {target}")

if errors:
    for e in errors:
        print(e)
    raise SystemExit(f"{len(errors)} broken link(s)")

print("links ok")
