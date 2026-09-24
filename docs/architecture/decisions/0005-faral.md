# ADR-0005: Format-Agnostic Routing Abstraction Layer (FARAL)

- **Status:** proposed
- **Date:** 2026-09-24

## Context

Routing tied to a specific map format locks in vendor and data source.

## Decision

Define a Unified Spatial Graph Interface (nodes, edges, weights, constraints,
temporal). Adapters for OSM, commercial, custom, and real-time data. Routing
algorithms operate on the interface, not the format.

## Consequences

- New data sources require new adapter, not new engine
- Small abstraction overhead per query
- Requires strict interface versioning
