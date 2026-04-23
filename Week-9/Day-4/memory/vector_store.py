"""
memory/vector_store.py

Vector Memory (FAISS)
- Converts text into embeddings
- Stores embeddings in a local FAISS index
- Retrieves semantically similar memories at query time
"""

import os
import json
import pickle
import numpy as np

try:
    import faiss
except ImportError:
    raise ImportError("Run: pip install faiss-cpu")

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    raise ImportError("Run: pip install sentence-transformers")

MEMORY_DIR = os.path.join(os.path.dirname(__file__), "..", "memory")
INDEX_PATH = os.path.join(MEMORY_DIR, "faiss.index")
META_PATH = os.path.join(MEMORY_DIR, "faiss_meta.pkl")
EMBED_MODEL = "all-MiniLM-L6-v2"
EMBED_DIM = 384

class VectorStore:
    """
    Local FAISS-based vector memory.
    """

    def __init__(self, persist: bool = True):
        self.persist = persist
        self.model = SentenceTransformer(EMBED_MODEL)
        self.metadata: list[dict] = []

        if persist and os.path.exists(INDEX_PATH) and os.path.exists(META_PATH):
            self._load()
        else:
            self.index = faiss.IndexFlatL2(EMBED_DIM)
            print(f"[INFO] New FAISS index created (dim={EMBED_DIM})")

    def _embed(self, text: str) -> np.ndarray:
        """Convert text to a normalised float32 embedding."""
        vec = self.model.encode([text], convert_to_numpy=True)
        return vec.astype(np.float32)

    def add(self, text: str, metadata: dict = None) -> int:
        """
        Embed text and add to the FAISS index.
        """
        from datetime import datetime

        vec = self._embed(text)
        self.index.add(vec)

        entry = {
            "text": text,
            "timestamp": datetime.now().isoformat(),
            **(metadata or {}),
        }
        self.metadata.append(entry)
        idx = len(self.metadata) - 1

        if self.persist:
            self.save()

        return idx

    def add_many(self, texts: list[str], metadata_list: list[dict] = None) -> list[int]:
        """Batch add multiple texts."""
        metadata_list = metadata_list or [{} for _ in texts]
        return [self.add(t, m) for t, m in zip(texts, metadata_list)]

    def search(self, query: str, top_k: int = 3) -> list[dict]:
        """
        Find top_k similar memories.
        """
        if self.index.ntotal == 0:
            return []

        top_k = min(top_k, self.index.ntotal)
        vec = self._embed(query)
        dists, indices = self.index.search(vec, top_k)

        results = []
        for rank, (dist, idx) in enumerate(zip(dists[0], indices[0])):
            if idx == -1:
                continue
            entry = dict(self.metadata[idx])
            entry["score"] = float(dist)
            entry["rank"] = rank + 1
            results.append(entry)

        return results

    def search_as_context(self, query: str, top_k: int = 3) -> str:
        """
        Search and return results formatted as a prompt context block.
        """
        results = self.search(query, top_k)
        if not results:
            return ""

        lines = ["=== Recalled from Vector Memory ==="]
        for r in results:
            lines.append(f"[{r['rank']}] (score={r['score']:.2f}) {r['text']}")
        return "\n".join(lines)

    def save(self):
        """Persist FAISS index and metadata to disk."""
        os.makedirs(MEMORY_DIR, exist_ok=True)
        faiss.write_index(self.index, INDEX_PATH)
        with open(META_PATH, "wb") as f:
            pickle.dump(self.metadata, f)

    def _load(self):
        """Load existing FAISS index and metadata from disk."""
        self.index = faiss.read_index(INDEX_PATH)
        with open(META_PATH, "rb") as f:
            self.metadata = pickle.load(f)
        print(f"[INFO] Loaded existing FAISS index: {self.index.ntotal} vectors")

    def stats(self) -> dict:
        return {
            "total_vectors": self.index.ntotal,
            "embed_model": EMBED_MODEL,
            "embed_dim": EMBED_DIM,
            "persisted": self.persist,
            "index_path": INDEX_PATH if self.persist else None,
        }

    def clear(self):
        """Wipe the index and metadata."""
        self.index = faiss.IndexFlatL2(EMBED_DIM)
        self.metadata = []
        if self.persist and os.path.exists(INDEX_PATH):
            os.remove(INDEX_PATH)
        if self.persist and os.path.exists(META_PATH):
            os.remove(META_PATH)
        print("[INFO] VectorStore index cleared.")
