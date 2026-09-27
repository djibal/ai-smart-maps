# A3 Report: Byzantine-Fault-Tolerant Community Reports

Config: 500 locations, 20 reporters, honest accuracy 85%,
20 trials. Byzantine strategies: random, invert, coordinated.

Pass criterion: at least one aggregator reaches >= 95% accuracy
under 30% Byzantine.

| Byzantine | Strategy | Majority | Supermajority | Reputation | Bayesian |
|---|---|---|---|---|---|
| 0% | random | 100.0% | 99.4% | 100.0% | 100.0% |
| 10% | random | 100.0% | 98.5% | 100.0% | 100.0% |
| 20% | random | 99.9% | 96.7% | 99.9% | 99.9% |
| 30% | random | 99.5% | 93.9% | 99.8% | 99.5% |
| 30% | invert | 92.5% | 73.4% | 99.8% | 92.5% |
| 30% | coordinated | 96.8% | 99.9% | 99.3% | 96.8% |

## Findings

- Best aggregator at 30% Byzantine: coordinated/supermajority at 99.9%.
- Pass criterion met: YES

## Verdict

**Overall A3: PASS**
