from sentence_transformers import SentenceTransformer, util


class TextRetriever:
    def __init__(self, documents):
        self.documents = documents
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        # Precompute embeddings
        self.embeddings = self.model.encode(documents, convert_to_tensor=True)

    def retrieve(self, query, top_k=2):
        query_embedding = self.model.encode(query, convert_to_tensor=True)

        scores = util.cos_sim(query_embedding, self.embeddings)[0]

        top_results = scores.topk(k=top_k)

        results = []
        score_list = []

        for idx in top_results.indices:
            results.append(self.documents[idx])
            score_list.append(float(scores[idx]))

        return {
            "data": "\n".join(results),
            "scores": score_list
        }