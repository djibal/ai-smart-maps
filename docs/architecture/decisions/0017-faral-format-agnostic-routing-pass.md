# ADR-0017: FARAL STRONG PASS — Format-Agnostic Routing Proven

- **Status:** accepted
- **Date:** 2026-09-29

## Context

ADR-0005 proposed a Format-Agnostic Routing Abstraction Layer (FARAL)
so that routing algorithms operate against a Unified Spatial Graph
Interface, not against any specific map format. This was flagged as a
medium-risk assumption: if routing could not be cleanly decoupled from
the data source, every new data format (commercial, real-time, custom)
would require rewriting the routing engine.

ADR-0016 (A6 partial pass) upgraded FARAL from an enhancement to a
critical dependency: the ~28% OSM freshness tail requires commercial
fallback, which requires the ability to plug in a commercial adapter
without touching the routing engine.

FARAL was therefore tested directly.

## Result

Four adapters were built behind the same interface:

- **OSMAdapter** — synthetic OSM-shaped graph, weight = distance
- **CommercialAdapter** — travel-time weights, road classes
- **RealTimeAdapter** — wraps any adapter, overlays hazards and closures
- **In-test ephemeral adapter** — defined inside a test file, never
  imported by the router

Metrics from a deterministic scenario:

| Adapter | Path length | Total cost |
|---|---|---|
| OSM | 12 | 1.4278 |
| Commercial | 9 | 0.0294 |
| RealTime (no updates) | 12 | 1.4278 |
| RealTime (with one closure) | 11 | 1.4664 |

## Claim verification

- **Router imports adapters?** Expected NO. Result: **PASS**.
  Verified by `grep -n "adapters\|osm\|commercial\|realtime" src/faral/router.py`
  returning no matches.
- **OSM and RealTime(empty) produce identical paths?** Expected YES.
  Result: **PASS**. Confirms the wrapper is transparent when there are
  no updates.
- **Same router works across all adapters?** Expected YES. Result:
  **PASS**. Four adapters, one Dijkstra implementation, all correct.

**Overall FARAL: STRONG PASS.**

## Findings

1. **The router is genuinely adapter-agnostic.** `router.py` imports
   only `heapq`, `math`, and `src.faral.interface`. It never references
   any adapter module. This is enforced by a grep check that is run on
   every commit.

2. **The zero-change proof works.** A new adapter was defined *inside a
   test file*, was never imported by the router, and the router routed
   correctly through it. This is the operational definition of the
   FARAL claim: adding a data source requires zero router changes.

3. **Different data sources produce different routes.** The Commercial
   adapter (travel-time weights) returns a 9-node path where OSM
   (distance weights) returns a 12-node path. Same source and
   destination, different optimal answer. This is the expected behavior
   and confirms that the adapter is not being bypassed.

4. **RealTime is a transparent wrapper.** With no updates, it produces
   bit-identical paths and costs to the base adapter. With one closure,
   it produces a longer, more expensive path — as expected.

5. **The interface is minimal.** Three methods (`nodes`, `edges`,
   `neighbors`) plus one free function (`effective_weight`) are enough
   to support routing across all data sources. No further abstraction
   is needed.

## Decision

**FARAL is validated. Adopt it as the routing architecture.**

- All routing algorithms must operate against `UnifiedSpatialGraph`.
- No routing code may import any adapter module.
- New data sources require only a new adapter, not router changes.
- The `source` field on each Edge preserves data lineage for audit and
  attribution.

The commercial-fallback dependency from ADR-0016 can now be implemented
as a `CommercialAdapter` plug-in. No routing engine changes required.

## Consequences

- **The critical dependency chain is unblocked.** ADR-0016 requires
  commercial fallback; FARAL provides the mechanism.
- **Adding new data sources is a bounded task.** A new adapter is
  100-200 lines of code, plus tests. Not a rewrite.
- **The interface is versioned.** Any change to `UnifiedSpatialGraph`
  is a breaking change and requires an ADR.
- **Real-time updates are transparent.** Hazard and closure overlays
  work as wrappers, not as router changes. This confirms the design
  for community-driven updates from A3.

## Scope of proof

Proven: the router is adapter-agnostic. Four adapters route correctly
against a single router with no adapter imports.

Not proven: real-world performance with commercial-scale graphs
(millions of nodes, tens of millions of edges). Memory and latency
characteristics of adapter-wrapping at scale. Adapter concurrency and
thread-safety. Real commercial API integration (schema, auth, rate
limits). These are implementation details, not architectural risks.
