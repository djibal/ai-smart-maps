"""Build a local RAG index over docs/ using Ollama embeddings.

Outputs:
  index/chunks.json   list of {id, source, heading, text}
  index/vectors.npz   float32 matrix aligned with chunks.json
"""
import json
from pathlib import Path

import numpy as np
import ollama

DOCS = Path("docs")
OUT = Path("index")
EMBED_MODEL = "nomic-embed-text"
CHUNK_CHARS = 800


def split_markdown(text):
    heading = ""
    buf = []
    for line in text.splitlines():
        if line.startswith("#"):
            heading = line.lstrip("# ").strip()
        buf.append(line)
        if sum(len(x) + 1 for x in buf) >= CHUNK_CHARS:
            yield heading, "\n".join(buf)
            buf = buf[-3:]
    if buf:
        yield heading, "\n".join(buf)


def main():
    OUT.mkdir(exist_ok=True)
    chunks = []
    for md in sorted(DOCS.rglob("*.md")):
        text = md.read_text(encoding="utf-8")
        for heading, body in split_markdown(text):
            body = body.strip()
            if len(body) < 40:
                continue
            chunks.append({
                "id": len(chunks),
                "source": str(md.relative_to(DOCS)),
                "heading": heading,
                "text": body,
            })

    if not chunks:
        raise SystemExit("no chunks found in docs/")

    vectors = []
    for c in chunks:
        r = ollama.embeddings(model=EMBED_MODEL, prompt=c["text"])
        vectors.append(r["embedding"])

    arr = np.asarray(vectors, dtype=np.float32)
    norms = np.linalg.norm(arr, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    arr = arr / norms

    (OUT / "chunks.json").write_text(json.dumps(chunks, indent=2), encoding="utf-8")
    np.savez_compressed(OUT / "vectors.npz", vectors=arr)
    print(f"indexed {len(chunks)} chunks from {len(list(DOCS.rglob('*.md')))} files")


if __name__ == "__main__":
    main()
