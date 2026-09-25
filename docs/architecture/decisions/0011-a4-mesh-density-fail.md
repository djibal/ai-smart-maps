# ADR-0011: A4 FAIL — Pure P2P BLE Cannot Deliver Sub-100ms at Urban Density

- **Status:** accepted
- **Date:** 2026-09-26

## Context

A4 tested whether BLE mesh at 1000 devices/km² can achieve sub-100ms
hazard propagation (blueprint mandate O6). The simulation used discrete-
event flood-fill with a duty-cycled scan model.

## Result

| Config | Radius | Duty | P95 latency | Reachable |
|---|---|---|---|---|
| urban_5pct_20m | 20m | 5% | inf | 0/30 |
| urban_10pct_20m | 20m | 10% | inf | 0/30 |
| urban_20pct_20m | 20m | 20% | inf | 0/30 |
| suburban_5pct_30m | 30m | 5% | inf | 0/30 |
| suburban_10pct_30m | 30m | 10% | inf | 0/30 |
| open_5pct_50m | 50m | 5% | 474 ms | 30/30 |
| open_10pct_50m | 50m | 10% | 271 ms | 30/30 |
| always_on_20m | 20m | 100% | inf | 0/30 |
| dense_urban_20pct | 20m | 20% | inf | 0/30 |
| sparse_suburban_10pct | 30m | 10% | inf | 0/30 |

**Overall A4: FAIL.**

## Findings

1. **Percolation threshold is ~38m.** For lambda = 0.001 devices/m^2,
   the 2D continuum percolation threshold is r_c = sqrt(4.51 / (pi * lambda))
   approximately 37.9m. Below 38m radius, the graph fragments. No duty
   cycle can fix this. The always_on_20m config confirms: even 100% duty
   cycle fails at 20m because no path exists.

2. **Duty cycle is not the bottleneck.** The blueprint assumed latency
   was dominated by scan wait. In fact, coverage dominates. At 50m
   radius (where the graph connects), duty cycling affects latency in
   the expected way: higher duty yields lower P95.

3. **At the smallest connecting radius (50m), latency is 200-470ms.**
   Path length is ~6 hops to cover 200m, and per-hop cost (tx + backoff
   + scan wait) accumulates. Sub-100ms is not achievable even at
   percolation threshold.

4. **Battery is not the constraint.** At 5% duty cycle, battery cost is
   0.41%/day, well under the 3% budget. This is the one assumption that
   A4 validated.

## Decision

Blueprint mandate O6 (sub-100ms peer-to-peer hazard propagation) is
**not achievable with pure P2P BLE at urban density.** The architecture
must adopt one of the following:

**Option A — Civic beacons required (recommended).**
Municipal fixed BLE nodes at intersections act as super-nodes. This
transforms the mesh from random P2P to infrastructure-backed, raising
effective density and eliminating the percolation gap. The blueprint's
A8 assumption (municipal adoption) becomes load-bearing, not optional.
Without civic beacons, O6 is unreachable.

**Option B — Revise O6 latency target.**
Change O6 from "sub-100ms" to "sub-500ms." Achievable at 50m radius
with 10% duty cycle (P95 = 271ms). Simple, no infrastructure required,
but weakens the safety promise.

**Option C — Hybrid: local BT plus cloud relay for city-wide.**
Sub-100ms within immediate neighborhood (single-hop, ~50m); 1-3s for
city-wide propagation via cloud. Preserves the local warning latency
while accepting cloud latency for broader coverage.

Recommended path: **Option A as the primary architecture, Option B as
the fallback if civic beacons fail to materialize.**

## Model limitations

This simulation does not capture:
- BLE 5 coded PHY (long range, up to 200m outdoors)
- Street geometry (devices along roads, not uniform 2D plane)
- Building attenuation (would make results worse, not better)
- Civic beacons (which would fix the percolation gap)

Future A4-v2 should add civic beacons and street geometry. The core
finding — that P2P BLE at 1000/km^2 cannot deliver sub-100ms — is
expected to hold.

## Consequences

- O6 must be revised in the blueprint or civic beacons must be
  guaranteed by business development.
- The mesh architecture in ADR-0004 (ZTMA) remains valid but must be
  deployed with civic-beacon support, not as a pure peer mesh.
- A8 (municipal adoption) is upgraded from "medium risk, nice to have"
  to "existential dependency."
- A4-v2 experiment planned: add civic beacons to the simulation and
  re-measure with infrastructure density of 10-50 beacons/km^2.
