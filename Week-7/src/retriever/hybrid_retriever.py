from rank_bm25 import BM25Okapi
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class HybridRetriever:
    def __init__(self, docs, embeddings_model, doc_embeddings):
        self.docs = docs
        self.model = embeddings_model
        self.doc_embeddings = doc_embeddings

        # BM25 setup
        tokenized_docs = [doc.split() for doc in docs]
        self.bm25 = BM25Okapi(tokenized_docs)

    def keyword_search(self, query, top_k=5):
        tokenized_query = query.split()
        scores = self.bm25.get_scores(tokenized_query)

        top_indices = np.argsort(scores)[::-1][:top_k]
        return [self.docs[i] for i in top_indices]

    def semantic_search(self, query, top_k=5):
        query_embedding = self.model.encode([query])
        scores = cosine_similarity(query_embedding, self.doc_embeddings)[0]

        top_indices = np.argsort(scores)[::-1][:top_k]
        return [self.docs[i] for i in top_indices]

    def hybrid_search(self, query, top_k=5):
        keyword_results = self.keyword_search(query, top_k)
        semantic_results = self.semantic_search(query, top_k)

        # Combine + remove duplicates
        combined = list(set(keyword_results + semantic_results))

        return combined[:top_k]