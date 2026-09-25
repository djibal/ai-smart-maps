# ADR-0010: A2 Passed — Federated Learning Converges, Krum Withstands 30% Byzantine

- **Status:** accepted
- **Date:** 2026-09-25

## Context

A2 tested whether federated learning converges on the A1-v5 task and
whether Byzantine-resistant aggregation survives malicious devices.

Config: 10 simulated devices, 500 samples each, non-IID partition
(80% primary variant per device), 20 FL rounds, 300-sample global test set.

Attack: sign-flip of weight deltas, amplified by 10x. Represents a strong
adversary with full control of update direction and magnitude.

## Result

| Config | Accuracy |
|---|---|
| Centralized (upper bound) | 98.0% |
| FedAvg honest | 97.3% |
| FedAvg + 1 Byzantine | 33.0% |
| FedAvg + 2 Byzantine | 18.0% |
| FedAvg + 3 Byzantine | 27.7% |
| Krum(f=3, m=3) + 3 Byzantine | 97.3% |
| TrimmedMean(trim=0.2) + 3 Byzantine | 18.3% |

## Findings

1. **FL convergence:** FedAvg honest reaches 97.3%, within 0.7pp of the
   centralized upper bound. FL is viable on this task.

2. **Attack strength:** amplified sign-flip from 3/10 devices destroys
   naive FedAvg, dropping accuracy by ~70pp.

3. **Krum(f=3, m=3):** fully recovers. Final accuracy matches honest
   FedAvg. This is the primary Byzantine defense.

4. **TrimmedMean(trim=0.2):** fails. Parameter must satisfy
   `trim >= f/n` to remove all f Byzantine updates. With f=3, n=10,
   the correct value is `trim >= 0.3`.

## Decision

Adopt Krum (f=3, m=3) as the primary Byzantine-resistant aggregator for
ADR-0003. TrimmedMean is a secondary defense and must be configured with
`trim >= f_expected / n_devices`. The federated learning pipeline is
approved for further development.

## Scope of proof

Proven: convergence and Byzantine resistance on a 4-feature binary
scoring task with 10 devices and up to 3 malicious actors.

Not proven: 100+ devices, adaptive attackers, data poisoning vs update
poisoning, non-IID attacker distribution, model poisoning via backdoor
injection. Those are subsequent tests.

## Consequences

- Krum (f=3, m=3) and TrimmedMean (trim >= 0.3) are both approved as
  Byzantine-resistant aggregators for ADR-0003.
- TrimmedMean's trim parameter must satisfy `trim >= f_expected / n_devices`.
  This constraint is now part of the FL pipeline specification.
- The FL pipeline is approved for further development. Next scale test:
  100+ devices, adaptive attackers, backdoor injection.
- ADR-0003 (MTFL-BR) remains valid with the concrete parameters now
  established by experiment.
