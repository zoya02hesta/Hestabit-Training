import faiss
import numpy as np
import os
import pickle

class FaissStore:
    def __init__(self, dim):
        self.index = faiss.IndexFlatL2(dim)
        self.texts = []

    def add(self, embeddings, texts):
        self.index.add(np.array(embeddings))
        self.texts.extend(texts)

    def save(self, path="src/vectorstore"):
        faiss.write_index(self.index, os.path.join(path, "index.faiss"))
        with open(os.path.join(path, "texts.pkl"), "wb") as f:
            pickle.dump(self.texts, f)

    def load(self, path="src/vectorstore"):
        self.index = faiss.read_index(os.path.join(path, "index.faiss"))
        with open(os.path.join(path, "texts.pkl"), "rb") as f:
            self.texts = pickle.load(f)

    def search(self, query_embedding, k=5):
        D, I = self.index.search(query_embedding, k)
        return [self.texts[i] for i in I[0]]