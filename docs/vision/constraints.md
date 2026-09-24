# Constraints

## Hard Constraints

| Constraint | Nature | Architectural Impact |
|------------|--------|---------------------|
| Battery budget | Hard (physics) | Max 3% daily BT+AI; adaptive duty cycling |
| Device storage | Hard (device) | Offline maps + models <2GB |
| On-device compute | Hard (hardware) | <500MB RAM; NPU/GPU execution |
| Privacy regulations | Legal | GDPR/CCPA/LGPD by design |
| Safety criticality | Ethical | Navigation errors can cause injury/death |
| Bluetooth interference | Physical | 2.4GHz congestion in dense areas |

## Soft Constraints

| Constraint | Nature | Impact |
|------------|--------|--------|
| GPS urban canyon | Environmental | BT positioning is fallback |
| Cross-platform parity | Business | iOS/Android/Web behavior identical |
| OSM data freshness | Data | Base layer lags commercial 6–18 months |
| Regulatory fragmentation | Legal | Per-country mapping restrictions |
