from src.embeddings.embedder import Embedder
from src.vectorstore.faiss_store import FaissStore
from src.retriever.hybrid_retriever import HybridRetriever
from src.retriever.reranker import Reranker
from src.pipelines.context_builder import ContextBuilder
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class TextRetriever:
    def __init__(self, documents=None):
        self.embedder = Embedder()
        self.store = FaissStore(384)
        try:
            self.store.load("src/vectorstore")
        except Exception as e:
            print(f"Could not load vector store: {e}")

        # Try to get raw docs and embeddings for advanced retrieval
        self.raw_docs = []
        for t in self.store.texts:
            chunk_text = t["text"] if isinstance(t, dict) and "text" in t else str(t)
            self.raw_docs.append(chunk_text)

        self.all_embeddings = np.array([])
        if self.store.index.ntotal > 0:
            self.all_embeddings = self.store.get_all_embeddings()
            self.hybrid = HybridRetriever(self.raw_docs, self.embedder.model, self.all_embeddings)
        else:
            self.hybrid = None
            
        self.reranker = Reranker()
        self.context_builder = ContextBuilder()

    def mmr(self, query_embedding, doc_embeddings, docs, top_k=5, diversity=0.5):
        if not docs:
            return []
        
        doc_embeddings = np.array(doc_embeddings)
        query_embedding = np.array(query_embedding).reshape(1, -1)
        
        sim_to_query = cosine_similarity(query_embedding, doc_embeddings)[0]
        
        selected_indices = [np.argmax(sim_to_query)]
        unselected_indices = list(range(len(docs)))
        unselected_indices.remove(selected_indices[0])
        
        for _ in range(min(top_k - 1, len(docs) - 1)):
            selected_embeddings = doc_embeddings[selected_indices]
            sim_to_selected = cosine_similarity(doc_embeddings[unselected_indices], selected_embeddings)
            max_sim_to_selected = np.max(sim_to_selected, axis=1)
            
            mmr_scores = (1 - diversity) * sim_to_query[unselected_indices] - diversity * max_sim_to_selected
            best_idx = unselected_indices[np.argmax(mmr_scores)]
            
            selected_indices.append(best_idx)
            unselected_indices.remove(best_idx)
            
        return [docs[i] for i in selected_indices]

    def retrieve(self, query, top_k=15):
        if not self.hybrid:
            # Fallback if store is empty or failed to load
            return {"data": "", "scores": []}

        # 1. Hybrid Search
        hybrid_docs = self.hybrid.hybrid_search(query, top_k=top_k*2)

        # 2. Rerank
        ranked_docs = self.reranker.rerank(query, hybrid_docs)
        
        # Take local top docs
        top_ranked_docs = ranked_docs[:top_k]
        
        # 3. Apply MMR on the top subset for diversity
        query_emb = self.embedder.embed([query])
        subset_embs = self.embedder.embed(top_ranked_docs) 
        mmr_docs = self.mmr(query_emb, subset_embs, top_ranked_docs, top_k=top_k)

        # 4. Deduplicate (though MMR inherently handles near duplicates, exact duplicates are filtered here)
        unique_docs = self.context_builder.deduplicate(mmr_docs)

        # 5. Build context optimally (limit length)
        # Assuming modern LLMs have at least 8k tokens, roughly 32000 chars. Set reasonable limit.
        context = self.context_builder.build_context(unique_docs, max_length=16000)

        # Dummy scores since we combined many strategies
        return {
            "data": context,
            "scores": [0.9] * len(unique_docs)
        }