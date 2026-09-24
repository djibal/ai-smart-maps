# High-Risk Assumptions

| ID | Assumption | Risk | Mitigation |
|----|-----------|------|------------|
| A1 | On-device AI matches cloud quality | High | Hybrid fallback; quality SLOs per mode |
| A2 | Federated learning converges at scale | High | Central validation; model canaries |
| A3 | Community contributes enough data | Medium | Gamification; seeding strategy |
| A4 | Mesh reaches critical density | High | Single-user value without mesh |
| A5 | BT battery impact <3% | Medium | Hardware co-processor; duty cycling |
| A6 | OSM made fresh enough | Medium | AI change detection; commercial fallback |
| A7 | Users trust privacy without audit | Medium | Third-party audits; open source core |
| A8 | Municipalities adopt civic beacons | Medium | B2B revenue model; pilot programs |
| A9 | Rivals won't copy features fast | High | Patents; network effects; open standard |
| A10 | Regulatory environment stable | Medium | Modular compliance layer per region |

**Existential:** A1, A2, A4, A9. Each requires a concrete architectural contingency.
