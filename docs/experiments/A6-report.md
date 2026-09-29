# A6 Report: OSM Freshness vs AI Change Detection

OpenStreetMap typically lags commercial maps by 6-18 months on road and
POI updates. Experiment A6 tests whether AI change detection from
satellite imagery and user reports can close that freshness gap relative
to raw OSM observation latency alone.

| Channel | Mean lag (days) | Detect within 90d |
|---|---|---|
| OSM | 358.1 | 2.1% ± 1.0% |
| Satellite | 15.1 | 49.1% ± 3.4% |
| User | 7.0 | 42.3% ± 3.1% |
| Combined | 109.6 | 71.6% ± 3.7% |

## Findings

- Raw OSM mean lag 358.1 days vs Combined mean lag 109.6 days (ratio Combined/OSM = 0.31).
- Combined detect within 90 days: 71.6%.
- mean_lag is averaged over DETECTED changes only. Combined mean can exceed individual channel means because combined includes slow channels' detections that single channels miss.

## Verdict

**Overall A6: PARTIAL PASS**

Combined channels detect 71.6% of changes within 90 days (71.6% 90-day detection rate).

## Design implication

The ~28% of changes not detected within 90 days require commercial fallback (per FARAL, ADR-0005) to reach the safety bar.
