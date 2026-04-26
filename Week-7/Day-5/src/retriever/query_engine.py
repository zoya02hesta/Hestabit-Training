from src.embeddings.embedder import Embedder
from src.vectorstore.faiss_store import FaissStore
import numpy as np

def query_rag(query):
    embedder = Embedder()

    store = FaissStore(dim=384)
    store.load()

    q_emb = embedder.embed([query])
    q_emb = np.array(q_emb)

    results = store.search(q_emb, k=5)

    return results


if __name__ == "__main__":
    query = input("Enter your query: ")
    results = query_rag(query)

    print("\nTop Results:\n")
    for i, r in enumerate(results):
        print(f"\n🔹 Result {i+1}")
        print(f"Source: {r['source']}")
        print(f"Chunk: {r['chunk_id']}")
        print(f"Text: {r['text'][:150]}...")