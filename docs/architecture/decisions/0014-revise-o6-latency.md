# ADR-0014: Revise O6 from Sub-100ms to Sub-500ms

- **Status:** accepted
- **Date:** 2026-09-27

## Context

Blueprint objective O6 originally promised "sub-100ms peer-to-peer hazard
propagation." The A4 series tested this claim:

- A4 (ADR-0011): pure P2P BLE at 1000 devices/km2 fails percolation
  below ~38m radius. No duty cycle fixes this.
- A4-v2 (ADR-0012): with 50 civic beacons/km2 and 100m beacon range,
  P95 = 95.3ms under ideal line-of-sight conditions. Margin: 4.7ms.
- A4-v3 (ADR-0013): attenuation factor 0.7 (mild urban) breaks the
  beacon grid's percolation. P95 = 906ms, 24/30 trials unreachable.
  Attenuation 0.5 (moderate urban) fully disconnects.

The A4-v2 PASS was a mathematical coincidence of the idealized model.
Real urban signal propagation includes buildings, foliage, weather, and
elevation — factors the model approximates as 0.5-0.7 range multipliers.
At those factors, sub-100ms is not achievable at economically viable
beacon density.

## Decision

Revise O6 from **sub-100ms** to:

- **Sub-500ms** peer-to-peer within a 200m radius, under realistic
  urban attenuation, at up to 50 beacons/km2
- **Sub-2s** city-wide via best-effort mesh or cloud relay
- **30% accident reduction** pilot target unchanged

The original sub-100ms promise is formally superseded.

## Rationale

1. **Sub-100ms is not achievable at viable cost.** The density required
   to maintain percolation under attenuation 0.5 is ~400 beacons/km2.
   In a 100 km2 city that is 40,000 units at $100-300 each — $4-12M per
   city, before operations.

2. **Sub-500ms retains the safety value.** A driver at 50 km/h travels
   6.9m in 500ms. Braking distance is ~30m. A 500ms warning is
   functionally equivalent to a 100ms warning for a human driver.

3. **Sub-2s city-wide is competitive.** No existing navigation product
   offers any peer-to-peer hazard warning. Sub-2s city-wide is
   dramatically better than the alternative (no warning at all).

4. **The revision is honest.** Promising sub-100ms in the blueprint and
   delivering sub-500ms in the product would be a marketing failure. The
   revised O6 is deliverable and defensible.

## Consequences

- **O6 in the objectives table is revised.** See `docs/vision/objectives.md`.
- **The risk register is updated.** "Mesh density insufficient" changes
  from "Resolved" to "Confirmed (no fix at viable cost)."
- **A8 (municipal adoption) remains existential** but at a lower
  threshold: ~50 beacons/km2 for best-effort mesh, not 400/km2.
- **Real-world pilot is required before product commitment.** The A4
  series uses an idealized model. Urban attenuation must be measured
  empirically in a pilot zone.
- **The safety promise in marketing must reflect sub-500ms, not
  sub-100ms.** This ADR is the authoritative source for that number.

## Scope

This ADR closes the A4 series. Further simulation without real hardware
will not produce new information. The next step is a hardware pilot in
one neighborhood, measuring actual BLE attenuation against the model's
assumptions.
