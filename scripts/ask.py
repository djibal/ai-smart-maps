"""Ask a question against the local docs RAG index.

Usage:
  python scripts/ask.py "What is DTF?"
"""
import json
import sys
from pathlib import Path

import numpy as np
import ollama

OUT = Path("index")
EMBED_MODEL = "nomic-embed-text"
GEN_MODEL = "llama3.2:3b"
TOP_K = 5
MIN_SIM = 0.30

SYSTEM = (
    "You are a documentation assistant for the AI-Smart-Maps project. "
    "Answer ONLY from the provided context. If the context does not contain "
    "the answer, reply exactly: Not found in documentation. "
    "Cite sources as [source: path]. Do not invent facts."
)


def load_index():
    chunks = json.loads((OUT / "chunks.json").read_text(encoding="utf-8"))
    vecs = np.load(OUT / "vectors.npz")["vectors"]
    return chunks, vecs


def retrieve(question, chunks, vecs):
    r = ollama.embeddings(model=EMBED_MODEL, prompt=question)
    q = np.asarray(r["embedding"], dtype=np.float32)
    q = q / max(np.linalg.norm(q), 1e-8)
    sims = vecs @ q
    idx = np.argsort(-sims)[:TOP_K]
    return [(float(sims[i]), chunks[i]) for i in idx]


def main():
    if len(sys.argv) < 2:
        print("usage: python scripts/ask.py your-question")
        raise SystemExit(2)

    if not (OUT / "chunks.json").exists():
        print("index missing. run: python scripts/build_index.py")
        raise SystemExit(2)

    question = " ".join(sys.argv[1:])
    chunks, vecs = load_index()
    hits = retrieve(question, chunks, vecs)

    if hits[0][0] < MIN_SIM:
        print("Not found in documentation.")
        return

    context = "\n\n".join(
        f"[source: {c['source']} | {c['heading']}]\n{c['text']}"
        for _, c in hits
    )

    resp = ollama.chat(
        model=GEN_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
        ],
    )
    print(resp["message"]["content"].strip())
    print("\n--- sources ---")
    for sim, c in hits:
        print(f"{sim:.3f}  {c['source']}  ({c['heading']})")


if __name__ == "__main__":
    main()
