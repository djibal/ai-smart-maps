# Logical Architecture

Layered view from the blueprint (Part III.1). Three tiers: Client, Edge, Core.

## Client Layer (Device)

- UI / UX Render
- Routing Engine (shared Rust core)
- AI Runtime (on-device inference)
- Mesh Protocol
- Map Cache (offline tiles)

All client components must function offline. The <100ms mesh requirement forces
edge-first processing with zero cloud dependency.

## Edge Layer (Regional)

- Tile Cache
- Route Cache
- Model Cache
- Mesh Relay
- Trust Service

Edge caches pre-compute popular routes and serve tiles geographically. Mesh relay
bridges cross-region traffic. Trust service evaluates community reports.

## Core Layer (Global)

- Map Data Store
- AI Training Pipeline
- Federated Learning
- Identity & Auth
- Billing & Subscription

Core operates with eventual consistency across regions. Each region is
self-sufficient under partition.

## Resilience Patterns

Circuit breaker, bulkhead, retry with backoff, fallback (cloud → device → cache),
strict timeouts, graceful degradation, idempotency, event sourcing, CQRS, saga.

## Related Decisions

- [ADR-0002 DTF](../architecture/decisions/0002-dtf.md) — decentralized tiles
- [ADR-0005 FARAL](../architecture/decisions/0005-faral.md) — format-agnostic routing
- [ADR-0006 TDLA](../architecture/decisions/0006-tdla.md) — temporal data lifecycle
