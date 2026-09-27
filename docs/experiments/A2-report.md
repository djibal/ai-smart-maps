# A2 Report: Federated Learning Convergence

Config: 10 devices, 500 samples/device, 20 FL rounds,
non-IID partition (80% primary variant, remainder split).
Attack: sign-flip scaled by 10x on weight deltas.

## Results

| Config | Final accuracy |
|---|---|
| Centralized (upper bound) | 98.0% |
| FedAvg, no attackers | 97.3% |
| FedAvg, 1 Byzantine | 33.0% |
| FedAvg, 2 Byzantine | 18.0% |
| FedAvg, 3 Byzantine | 27.7% |
| Krum(f=3,m=3), 3 Byzantine | 97.3% |
| TrimmedMean(trim=0.3), 3 Byzantine | 98.0% |

## Findings

- FL viability: FedAvg honest is 0.7pp below centralized. PASS (<= 5pp).
- FedAvg attack damage (3 Byzantine): 69.7pp.
- Krum recovery over undefended FedAvg+3byz: +69.7pp.
- TrimmedMean recovery over undefended FedAvg+3byz: +70.3pp.

## Verdict

- FL convergence: PASS
- Krum defense effective: PASS
- TrimmedMean defense effective: PASS

**Overall A2: PASS**
