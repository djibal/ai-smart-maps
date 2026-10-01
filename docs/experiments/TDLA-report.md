# TDLA Report: Temporal Data Lifecycle Architecture

TDLA (ADR-0006) proposes a four-tier temporal data lifecycle
(HOT/WARM/COLD/ARCHIVE) to bound storage and meet per-tier
latency SLOs.
This report tests both claims.

## Configuration

- Cities (n_cities): 100
- sim_days: 1095
- segment_km_per_city: 5000

## Storage

| Tier | Final count | Stored (PB) | Compression |
|---|---|---|---|
| HOT | 1345 | 0.00000003 | 1.0 |
| WARM | 14072 | 0.00000010 | 0.4 |
| COLD | 106727 | 0.00000010 | 0.05 |
| ARCHIVE | 60677 | 0.00000001 | 0.01 |

## Latency

| Tier | SLO (ms) | p95 (ms) | Verdict |
|---|---|---|---|
| HOT | 10.0 | 8.1 | PASS |
| WARM | 100.0 | 77.3 | PASS |
| COLD | 5000.0 | 4222.1 | PASS |
| ARCHIVE | 30000.0 | 24080.9 | PASS |

## Claim verification

- Storage converges?: PASS
- All latency SLOs met?: PASS

## Verdict

**Overall TDLA: STRONG PASS**

Storage stayed inside the convergence band and every tier met its latency SLO.
