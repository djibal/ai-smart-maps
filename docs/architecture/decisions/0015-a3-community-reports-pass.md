# ADR-0015: A3 PASS — Reputation-Weighted Aggregation for Community Reports

- **Status:** accepted
- **Date:** 2026-09-27

## Context

Blueprint mandate O5 promises a "Byzantine-fault-tolerant contribution
pipeline" with ">95% report accuracy at scale."

A3 tested four aggregation strategies against three Byzantine attack
strategies, at up to 30% malicious reporters:

- Honest reporter accuracy: 85% (independent errors)
- Reporters per trial: 20
- Locations per trial: 500
- Trials: 20 per config
- Attacks: random (coin flip), invert (always lie), coordinated (all report hazard)

## Result

| Byzantine | Majority | Supermajority | Reputation | Bayesian |
|---|---|---|---|---|
| 0% | 100.0% | 99.4% | 100.0% | 100.0% |
| 10% random | 100.0% | 98.5% | 100.0% | 100.0% |
| 20% random | 99.9% | 96.7% | 99.9% | 99.9% |
| 30% random | 99.5% | 93.9% | 99.8% | 99.5% |
| 30% invert | 92.5% | 73.4% | **99.8%** | 92.5% |
| 30% coordinated | 96.8% | 99.9% | 99.3% | 96.8% |

**Overall A3: PASS.**

## Findings

1. **Random Byzantine attacks are easily neutralized.** Every aggregator
   holds >= 93% against 30% random attackers. Coin-flipping attackers
   add noise but not signal bias.

2. **Adversarial (invert) attacks break naive aggregators.**
   - Majority: 92.5% (below the 95% target)
   - Supermajority: 73.4% (catastrophic)
   - Bayesian: 92.5%
   - **Reputation-weighted: 99.8%** (only aggregator above the target)

   The invert attack is the correct test for Byzantine tolerance because
   a real adversary does not produce random noise — they produce
   consistently wrong reports.

3. **Reputation-weighted is the only robust aggregator across all
   attack classes.** It scores 99.3-99.8% on every Byzantine config,
   with the smallest variance. This makes it the recommended default.

4. **Supermajority is a specialist, not a generalist.** It is best on
   coordinated attacks (99.9%) because a 2/3 threshold naturally rejects
   a coordinated 30% minority that always says the same thing. But it
   fails completely on invert (73.4%) because the attack looks like a
   coherent alternative position.

5. **Bayesian is no better than majority.** The naive Bayesian assumes
   reporter errors are independent with a known accuracy. Under
   adversarial attack, that assumption fails and Bayesian defaults to
   the same performance as majority.

## Decision

**Adopt reputation-weighted aggregation as the primary community-report
aggregation method.** This matches the pattern established in ADR-0010,
where Krum was adopted for federated learning aggregation.

The reputation update rule:

- Start all reporters at reputation = 1.0
- Each round, compute weighted consensus, then update each reporter
  by their agreement with consensus: agree -> reputation * 1.5,
  disagree -> reputation * 0.5
- Renormalize so the mean reputation stays at 1.0
- Iterate 3 rounds

This is a simple, interpretable rule with no learned parameters.

## Consequences

- **Community report pipeline is approved for further development.**
  The aggregation strategy is validated against three attack classes
  at up to 30% Byzantine.

- **The <95% accuracy risk in O5 is resolved for adversarial attacks.**
  Random noise was never the threat. Invert attacks were.

- **Reputation tracking is now a first-class subsystem.** It must be
  persistent, resistant to gaming (sybil resistance), and auditable.
  This is captured in the existing Trust Service component of the
  logical architecture.

- **A3-v2 with reputation gaming is planned.** The current simulation
  assumes attackers do not try to fake reputation — they just vote
  maliciously. A stronger adversary would attempt to earn reputation
  first, then attack. That is a separate experiment.

## Scope of proof

Proven: reputation-weighted aggregation reaches >= 99% verdict accuracy
against 30% random, invert, or coordinated Byzantine attackers on a
500-location, 20-reporter, 20-trial binary classification task.

Not proven: sybil attacks where the adversary creates many identities
to dominate reputation. Adaptive attackers who change strategy over
time. Reputation gaming across multiple rounds. Cross-location
correlations where the adversary exploits spatial structure.

These are subsequent experiments (A3-v2, A3-v3) and are expected to be
harder. The current result establishes the base case: reputation
weighting works when attackers are a fixed 30% minority.
