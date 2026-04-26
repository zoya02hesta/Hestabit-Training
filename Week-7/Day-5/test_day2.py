import numpy as np

from src.retriever.hybrid_retriever import HybridRetriever
from src.retriever.reranker import Reranker
from src.pipelines.context_builder import ContextBuilder


# -------------------------
# Sample Documents
# -------------------------
docs = [
    "Credit underwriting evaluates risk before lending.",
    "Banks analyze financial history and income.",
    "Policies define underwriting rules.",
    "Underwriting helps prevent loan defaults."
]


# -------------------------
# Dummy Embedding Model
# -------------------------
class DummyModel:
    def encode(self, texts):
        return np.array([[len(text)] for text in texts])


model = DummyModel()

doc_embeddings = np.array([[10], [20], [30], [40]])


# -------------------------
# Initialize Components
# -------------------------
retriever = HybridRetriever(docs, model, doc_embeddings)
reranker = Reranker()
context_builder = ContextBuilder()


# -------------------------
# Query
# -------------------------
query = "Explain credit underwriting"

results = retriever.hybrid_search(query)
print("\n🔹 Hybrid Results:")
print(results)


results = reranker.rerank(query, results)
print("\n🔹 After Reranking:")
print(results)


results = context_builder.deduplicate(results)
print("\n🔹 After Deduplication:")
print(results)


final_context = context_builder.build_context(results)

print("\n🔹 Final Context:\n")
print(final_context)
