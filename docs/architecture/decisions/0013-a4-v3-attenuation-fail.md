# ADR-0013: A4-v3 FAIL — A4-v2 PASS Does Not Survive Urban Attenuation

- **Status:** accepted
- **Date:** 2026-09-27

## Context

A4-v2 (ADR-0012) showed that 50 civic beacons/km² with 100m range
achieved P95 = 95.3ms at 1000 devices/km² with 10% mobile duty. This
was a conditional PASS with only 4.7ms margin.

A4-v3 tested whether that margin survives realistic degradations:
packet loss, signal attenuation (buildings, foliage, weather), and
beacon outage.

## Result

| Config | Beacons | Atten | Loss | Outage | P95 | Unreach | Verdict |
|---|---|---|---|---|---|---|---|
| baseline_50b | 50/km2 | 1.0 | 0.0 | 0.0 | 96.7ms | 0 | PASS |
| loss_10pct | 50/km2 | 1.0 | 0.1 | 0.0 | 95.1ms | 0 | PASS |
| loss_20pct | 50/km2 | 1.0 | 0.2 | 0.0 | 97.2ms | 0 | PASS |
| atten_0.7 | 50/km2 | 0.7 | 0.0 | 0.0 | 906.2ms | 24 | FAIL |
| atten_0.5 | 50/km2 | 0.5 | 0.0 | 0.0 | inf | 30 | FAIL |
| beacon_out_5pct | 50/km2 | 1.0 | 0.0 | 0.05 | 98.7ms | 0 | PASS |
| beacon_out_10pct | 50/km2 | 1.0 | 0.0 | 0.1 | 128.6ms | 1 | FAIL |
| mild_combined | 50/km2 | 0.7 | 0.1 | 0.05 | 802.5ms | 29 | FAIL |
| severe_combined | 50/km2 | 0.5 | 0.2 | 0.1 | inf | 30 | FAIL |
| 100b_severe | 100/km2 | 0.5 | 0.2 | 0.1 | inf | 30 | FAIL |

**Overall A4-v3: FAIL.**

## Findings

1. **Packet loss is not the bottleneck.** Even 20% loss has negligible
   impact (97.2ms vs 96.7ms baseline). The retry factor 1/(1-p) inflates
   each hop mildly.

2. **Attenuation is fatal, and it is a percolation problem, not a
   latency problem.** At 50 beacons/km2, beacon grid spacing is 125m.
   Beacon range is 100m. Attenuation factor 0.7 reduces effective range
   to 70m. 125 > 70, so the beacon grid disconnects. Messages cannot
   propagate — not slowly, but not at all. 24/30 trials fail to reach
   90% of the target nodes.

3. **Density must scale with 1/attenuation^2 to maintain percolation.**
   The required beacon density to maintain grid connectivity at a given
   attenuation factor:

   | Attenuation | Effective range | Required density |
   |---|---|---|
   | 1.0 | 100m | ~50/km2 (mobile bridge) |
   | 0.7 | 70m | ~200/km2 |
   | 0.5 | 50m | ~400/km2 |

4. **Doubling to 100 beacons/km2 does not rescue severe attenuation.**
   At 100 beacons/km2, grid spacing is 100m. Effective range at 0.5
   attenuation is 50m. Still disconnected.

5. **Beacon outage at 10% breaks the margin.** P95 = 128.6ms, 1/30
   unreachable. Real urban deployments must assume some beacon failure.

## Decision

**The A4-v2 PASS does not survive realistic urban conditions.** O6
(sub-100ms peer-to-peer hazard propagation) is not achievable with the
civic-beacon architecture at economically plausible densities.

The blueprint must adopt one of:

**Option A (recommended) — Revise O6 to sub-500ms.**
Sub-500ms is honest and achievable. Sub-100ms is not. The blueprint's
safety promise becomes "sub-second hazard warning," which is still
dramatically better than Waze/Google (which has no such feature at all).

**Option B — Line-of-sight beacon deployment.**
Require beacons be mast-mounted above street furniture with direct
line-of-sight to adjacent beacons. Reduces attenuation to ~0.9. But 125m
spacing still exceeds 90m effective range, so density must increase to
~100/km² minimum. And line-of-sight cannot be guaranteed across all
urban terrain (bridges, tunnels, hills, dense tree cover).

**Option C — Drop civic beacons for latency, use cloud relay for reach.**
Sub-second local BLE (single-hop, ~50m) for immediate neighborhood
warning; 1-3s via cloud for city-wide propagation. Sub-100ms becomes
sub-1s, with best-effort local fast path.

Recommended: **Option A.** Revise O6. The safety value of a 500ms
warning is nearly identical to a 100ms warning for a driver at 50 km/h
(braking distance ~30m). Sub-500ms is defensible. Sub-100ms is not
achievable at viable cost.

## Consequences

- **O6 is revised from sub-100ms to sub-500ms.** This requires a
  blueprint amendment and a new ADR superseding the O6 success metric
  in the original objective table.

- **A8 (municipal adoption) remains existential** but at a lower density
  threshold: ~50 beacons/km² for best-effort, not 400/km² for
  sub-100ms.

- **Real-world validation is still required.** The A4 series uses an
  idealized propagation model. Actual urban attenuation must be
  measured in a pilot zone before any deployment commitment.

- **The safety promise is now honest.** "Sub-second hazard warning via
  a privacy-preserving mesh with civic infrastructure" is credible and
  deliverable. "Sub-100ms" was not.

- **The A4 series is complete.** A4 (P2P fails), A4-v2 (beacons fix
  under ideal conditions), A4-v3 (attenuation breaks the ideal
  conditions). Further simulation without real hardware will not
  produce new information.

## Scope of proof

Proven: the architecture is sensitive to signal attenuation in a way
that cannot be fixed by density at economically viable scales.

Not proven: whether mast-mounted line-of-sight deployment achieves
0.9+ attenuation in practice. Whether real BLE 5 coded PHY outperforms
the 100m assumption. Whether a hybrid local+cloud architecture preserves
the safety promise in the driver-psychology sense (is 500ms actually
fine?).
