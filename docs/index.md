# AI-Smart-Maps

Intelligent documentation system for the AI-Smart-Maps blueprint.
Authored in Markdown, validated by schema and pytest, published via MkDocs.

## Sections

- **Vision** — [Objectives](vision/objectives.md), [Constraints](vision/constraints.md)
- **Architecture** — [Logical](architecture/logical.md), [Trade-offs](architecture/tradeoffs.md), [ADRs](architecture/decisions/index.md)
- **Risks** — [Assumptions](risks/assumptions.md), [Register](risks/register.md)
- **Roadmap** — [Phases](roadmap/phases.md), [Gates](roadmap/gates.md)
- **Knowledge** — [Local AI usage](knowledge/usage.md)
- **State** — [Ledger](_state/ledger.md)

## Scope

This repository documents the AI-Smart-Maps architecture. It does not implement
the navigation product. Product implementation (Rust core, ONNX runtime, BLE mesh,
federated learning) is a separate, code-first track.

## Validation

Every commit runs:

- UTF-8 normalization
- Required-file and orphan-link checks
- ADR frontmatter validation
- JSON schema parsing
- MkDocs strict build
- Pytest (docs, ADRs, links, RAG index)

Local AI queries are grounded strictly in `docs/`. Answers cite source files.
