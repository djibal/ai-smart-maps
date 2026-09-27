# Vision and Objectives

## Six Irreducible Mandates

| ID | Objective | Architectural Mandate | Success Metric |
|----|-----------|----------------------|----------------|
| O1 | AI-powered smart shortcuts | Real-time graph optimization with multi-objective cost functions | Route quality > Google/Waze in blind A/B tests |
| O2 | Privacy-first design | Zero-knowledge architecture; no PII at rest or in transit | Zero data-breach blast radius |
| O3 | Cross-platform delivery | Single logical system, multiple render targets | Feature parity within 2 weeks of release |
| O4 | Offline-full AI | On-device inference parity with cloud | <5% quality delta offline vs online |
| O5 | Community-powered data | Byzantine-fault-tolerant contribution pipeline | >95% report accuracy at scale |
| O6 | Bluetooth mesh safety (revised per ADR-0013) | Sub-500ms peer-to-peer within 200m; sub-2s city-wide via mesh or cloud | 30% accident reduction in pilot zones |

## Tension Web

Mandates are not independent:

- O2 (privacy) constrains O5 (community data)
- O4 (offline) limits AI model size, constraining O1 (shortcut quality)
- O6 (mesh latency) forces edge-first processing with zero cloud dependency

This tension is the central architectural challenge.


## O6 Revision Note

Original O6 (sub-100ms) was falsified by A4 and A4-v3. See ADR-0011 and ADR-0013. Revised target above reflects achievable latency under realistic urban propagation.
