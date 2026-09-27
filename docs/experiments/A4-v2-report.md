# A4-v2 Report: Civic Beacons in the Mesh

Same flood-fill model as A4, plus mains-powered civic beacons
(100m range, always on, on a grid). Metric: P95 latency for 90%
coverage of a 200m circle. Pass: P95 <= 100ms, all reachable,
mobile battery <= 3%/day.

| Config | Beacons | Beacon R | Mobile R | Mobile Duty | P50 | P95 | Unreach | Verdict |
|---|---|---|---|---|---|---|---|---|
| no_beacons_baseline | 0/km2 | 100m | 20m | 0.1 | infms | infms | 30 | FAIL |
| 10_beacons_20m_10pct | 10/km2 | 100m | 20m | 0.1 | infms | infms | 30 | FAIL |
| 20_beacons_20m_10pct | 20/km2 | 100m | 20m | 0.1 | infms | infms | 30 | FAIL |
| 50_beacons_20m_10pct | 50/km2 | 100m | 20m | 0.1 | 90.2ms | 95.3ms | 0 | PASS |
| 20_beacons_20m_5pct | 20/km2 | 100m | 20m | 0.05 | infms | infms | 30 | FAIL |
| 20_beacons_20m_20pct | 20/km2 | 100m | 20m | 0.2 | infms | infms | 30 | FAIL |
| 20_beacons_30m_10pct | 20/km2 | 100m | 30m | 0.1 | 365.5ms | 860.6ms | 2 | FAIL |
| 20_beacons_20m_10pct_50r | 20/km2 | 50m | 20m | 0.1 | infms | infms | 30 | FAIL |

## Verdict

**Overall A4-v2: PASS**
