# ADR-0009: A1 Passed — On-Device Scorer Within 3pp of Cloud

- **Status:** accepted
- **Date:** 2026-09-25

## Context

A1 tested whether a small learned scorer on-device can match a larger
cloud-side scorer on binary route cost comparison.

Five iterations:
- v1/v2: general-purpose LLMs (llama3.2:3b, qwen2.5:0.5b). Both below random.
  Null result. Led to ADR-0008.
- v3: small MLPs with MSE loss. Device falls behind on threshold variant (8.6pp).
- v4: same MLPs, pairwise margin ranking loss. Single-run results unstable
  (delta 2–16pp across variants).
- v5: 5 seeds per variant, device model grown 16x1 to 32x2, criterion on mean.

## Result

| Variant | Cloud | Device | Delta |
|---|---|---|---|
| linear | 99.7 +/- 0.2 | 98.5 +/- 0.7 | 1.2pp |
| quadratic | 99.6 +/- 0.2 | 98.5 +/- 0.6 | 1.0pp |
| threshold | 98.7 +/- 0.1 | 97.3 +/- 0.9 | 1.4pp |

Device model: 32 hidden, 2 layers, ~1000 parameters, ~4 KB on disk.

## Decision

A1 is passed. The architecture direction is: specialized on-device scorer,
trained with pairwise ranking loss, 32x2 MLP or equivalent.

## Scope of proof

Proven: small scorer matches cloud on a 4-feature binary route cost task
with three cost-function variants.

Not proven: real road-network routing with 50+ features, dynamic edge
weights, time-varying topology, million-user training scale. These are
subjects of A2 and later experiments.

## Consequences

- On-device scoring is viable within the target delta
- A2 (federated learning convergence) can proceed with confidence
- The blueprint's O4 (offline AI parity) has empirical support, not just theory
- ADR-0008 remains valid: no general-purpose LLM in the routing path
