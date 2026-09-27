# A4-v3 Report: Realistic Propagation

Same flood-fill as A4-v2, at the A4-v2 pass point (50 beacons/km2,
100m beacon range, 20m mobile range, 10% mobile duty), plus:

- Packet loss: per-hop retransmit factor 1/(1-p)
- Attenuation: all ranges multiplied by a factor (buildings, walls)
- Beacon outage: fraction of beacons offline per trial

Pass: P95 <= 100ms, all reachable, mobile battery <= 3%/day.

| Config | Beacons | Atten | Loss | Outage | P50 | P95 | Unreach | Verdict |
|---|---|---|---|---|---|---|---|---|
| baseline_50b | 50/km2 | 1.0 | 0.0 | 0.0 | 91.1ms | 96.7ms | 0 | PASS |
| loss_10pct | 50/km2 | 1.0 | 0.1 | 0.0 | 91.3ms | 95.1ms | 0 | PASS |
| loss_20pct | 50/km2 | 1.0 | 0.2 | 0.0 | 92.6ms | 97.2ms | 0 | PASS |
| atten_0.7 | 50/km2 | 0.7 | 0.0 | 0.0 | 495.0ms | 906.2ms | 24 | FAIL |
| atten_0.5 | 50/km2 | 0.5 | 0.0 | 0.0 | infms | infms | 30 | FAIL |
| beacon_out_5pct | 50/km2 | 1.0 | 0.0 | 0.05 | 91.0ms | 98.7ms | 0 | PASS |
| beacon_out_10pct | 50/km2 | 1.0 | 0.0 | 0.1 | 89.7ms | 128.6ms | 1 | FAIL |
| mild_combined | 50/km2 | 0.7 | 0.1 | 0.05 | 802.5ms | 802.5ms | 29 | FAIL |
| severe_combined | 50/km2 | 0.5 | 0.2 | 0.1 | infms | infms | 30 | FAIL |
| 100b_severe_combined | 100/km2 | 0.5 | 0.2 | 0.1 | infms | infms | 30 | FAIL |

## Findings

- Baseline reproduces A4-v2: P95=96.7ms, all reachable.
- Packet loss (20%) has negligible impact: P95=97.2ms.
- **Attenuation 0.7 (mild urban) breaks percolation:** P95=906.2ms, 24/30 unreachable.
- **Attenuation 0.5 (moderate urban) fully disconnects:** inf, 30/30.
- Mild combined degradation (atten 0.7 + loss 10% + outage 5%) fails: 29/30 unreachable.
- Doubling density to 100 beacons/km2 does NOT rescue severe attenuation (30/30 unreachable).

## Verdict

**Overall A4-v3: FAIL**

The A4-v2 PASS holds only under near-line-of-sight conditions. Any meaningful urban attenuation breaks the beacon grid's percolation.
