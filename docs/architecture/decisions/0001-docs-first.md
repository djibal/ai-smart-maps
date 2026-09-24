# ADR-0001: Documentation-First Authoring

- **Status:** accepted
- **Date:** 2026-09-24

## Context

The AI-Smart-Maps blueprint requires Rust, ONNX, BLE mesh, federated learning,
and edge infrastructure. No-code tooling cannot build that. But the blueprint
itself is unstructured, contains encoding corruption, and lacks API contracts,
schemas, and phase-gate criteria.

## Decision

Author all architectural documentation in Markdown + Git + MkDocs Material.
Treat the blueprint as source material, not as an implementation target.
No-code applies to documentation authoring only.

## Consequences

- Fast iteration on structured docs
- Validation via schemas and pytest
- Product implementation remains a separate, code-first track
