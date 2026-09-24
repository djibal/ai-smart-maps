# Local AI Knowledge Layer

Ground a local LLM in docs/ only. Answers cite source files. Refuses when
the docs do not contain the answer.

## Prerequisites

Install Ollama and pull two models:

    brew install ollama
    brew services start ollama
    ollama pull llama3.2:3b
    ollama pull nomic-embed-text

## Build the index

    make index

Writes index/chunks.json and index/vectors.npz. Rebuild after docs change.

## Ask

    make ask Q="What is Decentralized Tile Federation?"

or directly:

    python scripts/ask.py "What is Decentralized Tile Federation?"

Output: answer with [source: ...] citations plus a ranked source list.

## Grounding rules

- Answer strictly from retrieved chunks.
- If top similarity is below 0.35, print Not found in documentation.
- Never invent ADRs, risks, or phases not present in docs/.
