# ADR-0012: A4-v2 Conditional PASS — Civic Beacons Fix the Mesh at 50/km²

- **Status:** accepted
- **Date:** 2026-09-26

## Context

A4 (ADR-0011) showed that pure P2P BLE at 1000 devices/km² cannot deliver
sub-100ms hazard propagation. A4-v2 tests whether civic beacons (fixed,
mains-powered, on a grid) close the percolation gap.

Model: same flood-fill as A4, plus N beacons/km² with 100m range and 100%
duty. Mobile devices: 1000/km², 20-30m range, 5-20% duty.

## Result

| Config | Beacons | Beacon R | Mobile R | Duty | P50 | P95 | Unreach | Verdict |
|---|---|---|---|---|---|---|---|---|
| no_beacons_baseline | 0/km2 | 100m | 20m | 10% | inf | inf | 30/30 | FAIL |
| 10_beacons_20m | 10/km2 | 100m | 20m | 10% | inf | inf | 30/30 | FAIL |
| 20_beacons_20m | 20/km2 | 100m | 20m | 10% | inf | inf | 30/30 | FAIL |
| **50_beacons_20m** | **50/km2** | **100m** | **20m** | **10%** | **90.2ms** | **95.3ms** | **0/30** | **PASS** |
| 20_beacons_20m_5pct | 20/km2 | 100m | 20m | 5% | inf | inf | 30/30 | FAIL |
| 20_beacons_20m_20pct | 20/km2 | 100m | 20m | 20% | inf | inf | 30/30 | FAIL |
| 20_beacons_30m_mobile | 20/km2 | 100m | 30m | 10% | 365.5ms | 860.6ms | 2/30 | FAIL |
| 20_beacons_50m_beacon | 20/km2 | 50m | 20m | 10% | inf | inf | 30/30 | FAIL |

**Overall A4-v2: conditional PASS.**

Connectivity diagnostic (largest connected component):

| Config | Largest component |
|---|---|
| no_beacons | 21/1000 (2.1%) |
| 10 beacons/km2 | 48/1016 (4.7%) |
| 20 beacons/km2 | 106/1025 (10.3%) |
| **50 beacons/km2** | **1064/1064 (100%)** |
| 100 beacons/km2 | 1100/1100 (100%) |

## Findings

1. **Percolation threshold is ~50 beacons/km².** Below 50/km², the beacon
   grid is disconnected (spacing > beacon range) and mobile devices cannot
   bridge the gaps. Above 50/km², percolation holds.

2. **Beacon range matters more than mobile duty.** With 20/km² and 50m
   beacon range, coverage fails at every duty cycle tested. With the same
   density and 100m beacon range, coverage still fails — but at 50/km²
   with 100m range, it passes cleanly.

3. **Mobile duty cycle is not the constraint.** Even 5% duty would pass
   latency if connectivity existed (the failure at 20/km² + 5% is
   connectivity, not latency). Battery at 10% duty is 0.81%/day, well
   under the 3% budget.

4. **The margin is tight.** P95 = 95.3ms against a 100ms target — 4.7ms
   of headroom. Any real-world degradation (buildings, interference,
   beacon outage) could push it over.

## Decision

O6 (sub-100ms peer-to-peer hazard propagation) is **conditionally achievable**,
but only with:

- **Civic beacon density ≥ 50 beacons/km²** in urban zones
- **Beacon range ≥ 100m** (BLE 5 coded PHY, mains-powered)
- **Mobile duty cycle ≥ 10%** (battery cost 0.81%/day, well within budget)

If any of these conditions is not met, O6 fails and must be revised
to sub-500ms (see ADR-0011 Option B).

## Consequences

- **A8 (municipal adoption) is upgraded from "medium risk" to "existential
  dependency."** Without municipal deployment of civic beacons at ≥50/km²,
  O6 cannot be delivered.

- **Economic viability must be validated.** 50 beacons/km² in a 100 km²
  city = 5,000 units. At $100-300 per unit including installation, that
  is $500k-$1.5M per city. This is a business-development cost, not a
  software cost.

- **The tight margin requires real-world validation.** A4-v2 uses an
  idealized propagation model. Real-world BLE in dense urban environments
  (2.4 GHz congestion, buildings, interference) will be worse. A hardware
  pilot in one zone is required before city-wide commitment.

- **Fallback plan stands.** If beacon deployment fails economically or
  politically, revise O6 to sub-500ms per ADR-0011 Option B. The
  architecture in ADR-0004 (ZTMA) remains valid; only the safety promise
  changes.

- **Next experiment: A4-v3 with realistic propagation.** Add signal
  attenuation, packet loss, and beacon outage to the model. If P95 stays
  under 100ms with 20% loss and 10% beacon outage, O6 is robust. If not,
  the tight margin becomes a real risk.

## Scope of proof

Proven: idealized propagation with a grid of civic beacons reaches
sub-100ms at 50 beacons/km² with 100m range.

Not proven: real-world propagation with buildings, interference, packet
loss, beacon failure. Real hardware BLE behavior at scale. Municipal
willingness to deploy 50 beacons/km². Cost effectiveness.
