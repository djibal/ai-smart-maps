# ADR-0008: Specialized On-Device Scorer, Not an LLM

- **Status:** accepted
- **Date:** 2026-09-25

## Context

A1 tested whether a small on-device LLM (qwen2.5:0.5b) can match a larger
cloud LLM (llama3.2:3b) on binary route cost comparison.

Result (100 scenarios, 5-route and 2-route variants):
- Cloud llama3.2:3b: 40–43% agreement with oracle (below random)
- Device qwen2.5:0.5b: 63% agreement, but only because it always answers "A"
- Neither model executes the required symbolic cost loop

Conclusion: general-purpose LLMs are the wrong architecture for route
optimization. The task requires edge lookups and arithmetic that LLMs
cannot perform reliably in a single forward pass.

## Decision

On-device AI for AI-Smart-Maps will use a purpose-built scorer
(small MLP, GNN, or gradient-boosted tree), trained to predict route
cost from graph features. No general-purpose LLM will run in the
routing decision path.

LLMs may still be used for:
- Natural-language interaction with the user (voice, chat)
- Summarizing community reports
- Assisting map annotation on the cloud side

They will not be used for cost comparison or route optimization.

## Consequences

- On-device AI footprint drops by 100x–1000x (KB vs GB)
- Inference latency drops from hundreds of ms to sub-ms
- Training pipeline must produce labeled route/cost pairs
- A1 must be re-run with a scorer (see A1-v3)
- Supersedes the LLM-based assumption in ADR-0007
