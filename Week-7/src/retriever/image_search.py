import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


class ImageSearch:
    def __init__(self, data):
        self.data = data

    def search_by_text(self, query_embedding, top_k=3):
        embeddings = [item["embedding"] for item in self.data]

        scores = cosine_similarity([query_embedding], embeddings)[0]

        top_indices = np.argsort(scores)[::-1][:top_k]

        return [self.data[i] for i in top_indices]

    def search_by_image(self, image_embedding, top_k=3):
        embeddings = [item["embedding"] for item in self.data]

        scores = cosine_similarity([image_embedding], embeddings)[0]

        top_indices = np.argsort(scores)[::-1][:top_k]

        return [self.data[i] for i in top_indices]