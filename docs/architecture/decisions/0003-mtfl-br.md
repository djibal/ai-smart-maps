# ADR-0003: Multi-Tier Federated Learning with Byzantine Resistance (MTFL-BR)

- **Status:** proposed
- **Date:** 2026-09-24

## Context

Naive federated learning is vulnerable to model poisoning. No convergence
guarantees. Debugging is near-impossible.

## Decision

Four tiers: device updates (DP noise), regional aggregation (Krum / trimmed mean),
global synthesis (golden dataset validation), canary deployment (1% rollout with
auto-rollback).

## Consequences

- Byzantine resistance at regional tier
- Full model lineage for audit
- Slower convergence than naive FL
- Requires golden dataset maintenance
