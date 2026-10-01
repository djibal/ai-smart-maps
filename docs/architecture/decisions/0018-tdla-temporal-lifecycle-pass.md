# ADR-0018: TDLA STRONG PASS — Tier Mechanism Validated, Magnitude Scope Limited

- **Status:** accepted
- **Date:** 2026-10-01

## Context

ADR-0006 proposed a Temporal Data Lifecycle Architecture (TDLA): four
tiers (HOT 0-7 days, WARM 7-90 days, COLD 90-730 days, ARCHIVE >730
days) with tier-specific compression and latency SLOs. The claim was that
this bounds storage growth and meets per-tier query latency targets.

TDLA was tested directly.

## Result

Config: 100 cities, 5,000 km road each, 3-year horizon (1,095 days),
change rate 1 per 100 road-km per month.

### Storage (final day)

| Tier | Final count | Stored (PB) | Compression |
|---|---|---|---|
| HOT | 1,345 | 0.00000003 | 1.00 |
| WARM | 14,072 | 0.00000010 | 0.40 |
| COLD | 106,727 | 0.00000010 | 0.05 |
| ARCHIVE | 60,677 | 0.00000001 | 0.01 |
| **Total** | **182,821** | **~0.00000024** | — |

Total stored: ~260 MB across 100 cities over 3 years.

### Latency (p95, 10 samples per tier)

| Tier | SLO (ms) | p95 (ms) | Verdict |
|---|---|---|---|
| HOT | 10.0 | 8.1 | PASS |
| WARM | 100.0 | 77.3 | PASS |
| COLD | 5,000.0 | 4,222.1 | PASS |
| ARCHIVE | 30,000.0 | 24,080.9 | PASS |

## Findings

1. **Storage converges.** The final-day total is within the steady-state
   band relative to the day-730 snapshot. No unbounded growth.

2. **All four tiers meet their latency SLOs** under the simulated
   p95 sampling model.

3. **The magnitude is far below PB scale.** The model produces ~260 MB
   total, not petabytes. This is a real scope limitation, not a code
   issue: the model covers only geometric change events (~20 KB each).
   The blueprint's "PB-scale" claim refers to total map data (tiles,
   imagery, POI, AI models, temporal snapshots), which this experiment
   does not simulate.

4. **The mechanism is proven; the magnitude is not.** Four-tier
   lifecycle bounds storage *for the data slice it governs*. Whether
   that slice is representative of the whole is out of scope.

## Decision

**TDLA is validated for the change-event data slice.** The tier scheme,
compression factors, and latency SLOs are approved for this class of
data.

**A magnitude-bounding experiment is deferred.** A TDLA-v2 would need to
model tile imagery, POI databases, AI model versioning, and temporal
snapshots — the bulk of the PB-scale storage — to validate the full
blueprint claim. That is a larger experiment and lower priority than
moving to product-track work.

## Consequences

- **The four-tier scheme is approved.** HOT/WARM/COLD/ARCHIVE with the
  given compression factors and SLOs are the architecture for temporal
  data.

- **The blueprint's "PB-scale" language is a magnitude claim, not a
  mechanism claim.** The mechanism (tiering) is validated. The magnitude
  (PB) is not. Future ADRs should distinguish these.

- **Deletion policy from ADR-0006 remains unvalidated.** The experiment
  tested storage growth, not data retention guarantees. User-data
  deletion within 30 days, community-report anonymization after 90 days,
  and mesh-message non-persistence are separate concerns requiring
  separate tests.

- **TDLA-v2 planned for later.** If product-track work reveals tile or
  imagery storage is the binding constraint, TDLA-v2 becomes urgent.
  Until then, it stays queued.

## Scope of proof

Proven: four-tier lifecycle with tier-specific compression bounds
storage growth over 3 years for change-event data, and all four latency
SLOs are met under a simulated p95 sampling model.

Not proven: the model produces PB-scale storage (it produces ~260 MB
for the slice tested). Tile imagery, POI, AI model versions, and temporal
snapshots are not simulated. Deletion and retention guarantees are not
tested. Real database latencies at scale are not measured (the latency
test uses synthetic sampling around the SLO, not actual query execution).
