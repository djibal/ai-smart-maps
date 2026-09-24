# Phase Gates

Each phase requires explicit go/no-go review by the Architecture Review Board.

## Gate Criteria

| Phase | Must Pass Before Advancing |
|-------|---------------------------|
| P0 Foundation | Blueprint reviewed; docs scaffold builds; validator passes |
| P1 Core | Routing engine alpha with 1K users; latency budgets met |
| P2 AI | On-device inference <5% quality delta; canary pipeline live |
| P3 Mesh | <100ms hazard propagation in pilot zone; battery <3%/day |
| P4 Scale | 1M users, 10 cities; edge caches stable under 10M req/s peak |
| P5 Evolve | Global deployment; independent security audit passed |

## Conditional Advance

A phase may advance conditionally if:
- All critical risks have mitigations in place
- No unresolved existential assumption (A1, A2, A4, A9)
- Architecture Review Board records the exception
