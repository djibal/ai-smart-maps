import json
import re
from pathlib import Path

REQUIRED_FIELDS = ["status", "date", "context", "decision", "consequences"]
VALID_STATUS = {"accepted", "proposed", "rejected", "superseded", "deprecated"}

adr_dir = Path("docs/architecture/decisions")
files = sorted(p for p in adr_dir.glob("*.md") if re.match(r"^\d{4}-", p.name))
assert files, "no ADR files found"

for p in files:
    text = p.read_text(encoding="utf-8")
    for field in REQUIRED_FIELDS:
        assert field.lower() in text.lower(), f"{p}: missing {field}"
    m = re.search(r"\*\*Status:\*\*\s*(\w+)", text)
    assert m, f"{p}: no status line"
    assert m.group(1) in VALID_STATUS, f"{p}: invalid status {m.group(1)}"

# Validate schemas parse as JSON
for s in Path("schemas").glob("*.json"):
    json.loads(s.read_text(encoding="utf-8"))

print(f"adrs ok ({len(files)} files), schemas ok")
