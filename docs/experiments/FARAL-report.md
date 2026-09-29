# FARAL Report: Format-Agnostic Routing Layer

FARAL (ADR-0005) claims that routing algorithms operate on a Unified
Spatial Graph Interface, independent of the underlying data source.
This report tests that claim by routing the same query across OSM,
commercial, and real-time adapters with a single router implementation.

| Adapter | Path length | Total cost |
|---|---|---|
| OSM | 12 | 1.4278 |
| Commercial | 9 | 0.0294 |
| RealTime (no updates) | 12 | 1.4278 |
| RealTime (with one closure) | 11 | 1.4664 |

## Claim verification

- Router imports adapters? (expected NO): PASS
- OSM and RealTime(empty) produce identical paths? (expected YES): PASS
- Same router works across all adapters? (expected YES): PASS

## Verdict

**Overall FARAL: STRONG PASS**

The same Dijkstra router routes correctly across OSM, commercial, and real-time wrappers without importing any adapter.
