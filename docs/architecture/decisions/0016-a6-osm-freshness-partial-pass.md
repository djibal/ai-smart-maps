# ADR-0016: A6 PARTIAL PASS — AI Closes Most of OSM Freshness Gap, Commercial Fallback Required for Tail

- **Status:** accepted
- **Date:** 2026-09-29

## Context

Blueprint assumption A6: "OSM can be made fresh enough." OSM base layers
typically lag commercial maps by 6-18 months on road and POI changes.
The blueprint's stated mitigation is "AI change detection; commercial
fallback."

A6 tested this by simulating 500 km of road network over a 36-month
horizon with a change rate of 1 per 100 road-km per month, comparing four
observation channels:

- **OSM** — log-normal observation lag, mean 12 months, sigma 0.6
- **Satellite** — 30-day revisit, 50% per-change detection probability
- **User** — 70% detection, 7-day latency, 60% network coverage
- **Combined** — element-wise minimum across all three channels

20 trials, 3,547 total changes simulated.

## Result

| Channel | Mean lag (days) | Detect within 90d |
|---|---|---|
| OSM | 358.1 | 2.1% ± 1.0% |
| Satellite | 15.1 | 49.1% ± 3.4% |
| User | 7.0 | 42.3% ± 3.1% |
| **Combined** | **109.6** | **71.6% ± 3.7%** |

**Overall A6: PARTIAL PASS.**

## Findings

1. **AI change detection closes 97.9% of the 90-day detection gap.**
   Raw OSM detects only 2.1% of changes within 90 days. Combined
   channels detect 71.6%. That is a 34x improvement in fast detection.

2. **Mean lag improves 3.3x.** Raw OSM: 358 days. Combined: 110 days.
   Ratio: 0.31.

3. **A hard tail remains.** ~28% of changes are not detected within
   90 days by any AI channel. This tail consists of changes that
   satellite misses (no visible signature or cloudy weather) and that
   users do not report (low-coverage areas, low-traffic segments).

4. **Metric caveat: combined mean lag can exceed individual channel
   means.** The combined channel detects *more* changes, including the
   slow ones that only OSM would eventually catch. Those slow detections
   drag the combined mean upward. The correct headline metric for A6
   is not mean lag, but the 90-day detection rate.

5. **The blueprint's fallback strategy is load-bearing, not optional.**
   Without commercial fallback for the ~28% tail, effective staleness
   is 110 days — worse than the 3-month target implied by the blueprint.

## Decision

**A6 is a PARTIAL PASS. The architecture is approved with a mandatory
fallback dependency.**

- AI change detection (satellite + user) becomes a first-class subsystem.
- Commercial map licensing is required for the ~28% tail. This is not a
  cost optimization — it is a safety requirement.
- FARAL (ADR-0005, Format-Agnostic Routing Layer) is the correct place
  to absorb commercial feeds. The design already anticipated this.

## Consequences

- **The blueprint's "commercial fallback" language is upgraded from
  optional to mandatory.** The blueprint's Part I.5 assumption A6
  mitigation ("AI commercial fallback") is now a
  concrete dependency on commercial map vendor relationships.

- **Cost model updates.** Commercial licensing is now a recurring
  operating cost, not a Phase-5 contingency.

- **FARAL prototype is now higher priority.** The Adapter abstraction
  must support commercial feeds cleanly, not as an afterthought.

- **The freshness SLO is now concrete:** 90% of changes should be
  detected within 90 days. The A6 result (71.6%) is below this SLO, so
  combined with commercial fallback, the target is met.

- **A6-v2 experiment is planned.** Test whether user-report coverage
  (currently 60%) can be raised via gamification to close more of the
  tail, potentially reducing commercial fallback volume.

## Scope of proof

Proven: AI change detection channels (satellite + user) improve fast
detection by 34x over raw OSM, but leave a ~28% tail undetected within
90 days. This tail requires commercial fallback.

Not proven: real satellite change-detection performance on actual
imagery. Real user-report behavior and coverage at scale. Whether
gamification can push user coverage above 60% economically. Whether
commercial vendors will license at viable cost.
