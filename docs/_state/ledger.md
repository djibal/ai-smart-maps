# State Ledger

- Phase: 5
- Status: complete
- Decisions: docs-first, no-code authoring, UTF-8 normalization, local RAG grounded in docs/
- Completed:
  - P0 foundation (MkDocs, validators, pytest)
  - P1 structured vision, constraints, trade-offs, risks, roadmap
  - P2 ADRs, JSON schemas, phase gates, ADR validator
  - P3 pre-commit, CI workflow, link check, Makefile
  - P4 local RAG knowledge layer (Ollama + numpy)
  - P5 landing page, logical architecture, deploy to GitHub Pages
- Out of scope: product implementation (Rust, ONNX, BLE mesh, federated learning)
- Next: product track (separate repo)

## Experiment Track (separate repo: ai-smart-maps-a1)

- A1: on-device scorer within 3pp of cloud — PASS (ADR-0009)
- A2: federated learning converges, Krum withstands 30% Byzantine — PASS (ADR-0010)
- A4: pure P2P BLE cannot deliver sub-100ms at urban density — FAIL (ADR-0011)
- A9: competitive moat — not yet tested (business)

Next: A4-v2 with civic beacons, OR pause.
