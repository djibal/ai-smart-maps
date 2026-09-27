# A4 Report: Mesh Density Simulation

Flood-fill broadcast over duty-cycled BLE mesh.
Metric: P95 time for 90% of nodes within 200m of source.
Pass: P95 <= 100ms AND battery <= 3%/day AND unreachable == 0.

| Config | Density | Radius | Duty | Battery | P50 | P95 | Unreach | Verdict |
|---|---|---|---|---|---|---|---|---|
| urban_5pct_20m | 1000/km2 | 20m | 0.05 | 0.41% | infms | infms | 30 | FAIL |
| urban_10pct_20m | 1000/km2 | 20m | 0.1 | 0.81% | infms | infms | 30 | FAIL |
| urban_20pct_20m | 1000/km2 | 20m | 0.2 | 1.61% | infms | infms | 30 | FAIL |
| suburban_5pct_30m | 1000/km2 | 30m | 0.05 | 0.41% | infms | infms | 30 | FAIL |
| suburban_10pct_30m | 1000/km2 | 30m | 0.1 | 0.81% | infms | infms | 30 | FAIL |
| open_5pct_50m | 1000/km2 | 50m | 0.05 | 0.41% | 259.8ms | 474.0ms | 0 | FAIL |
| open_10pct_50m | 1000/km2 | 50m | 0.1 | 0.81% | 208.4ms | 270.7ms | 0 | FAIL |
| always_on_20m | 1000/km2 | 20m | 1.0 | 8.00% | infms | infms | 30 | FAIL |
| dense_urban_20pct | 2000/km2 | 20m | 0.2 | 1.61% | infms | infms | 30 | FAIL |
| sparse_suburban_10pct | 500/km2 | 30m | 0.1 | 0.81% | infms | infms | 30 | FAIL |

**Overall A4: FAIL**
