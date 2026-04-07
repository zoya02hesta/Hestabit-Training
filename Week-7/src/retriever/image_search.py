from sentence_transformers import SentenceTransformer, util
import torch


class ImageSearch:
    def __init__(self, data):
        self.data = data
        self.model = SentenceTransformer("clip-ViT-B-32")

    def search(self, query, top_k=2):
        if not self.data:
            return []

        query_embedding = self.model.encode(query, convert_to_tensor=True)

        image_embeddings = torch.stack([
            item["embedding"] if torch.is_tensor(item["embedding"])
            else torch.tensor(item["embedding"])
            for item in self.data
        ])

        scores = util.cos_sim(query_embedding, image_embeddings)[0]

        top_results = torch.topk(scores, k=min(top_k, len(self.data)))

        results = []

        for idx, score in zip(top_results.indices, top_results.values):
            item = self.data[idx]

            results.append({
                "image": item.get("image_path", ""),
                "caption": item.get("caption", ""),
                "ocr": item.get("ocr", ""),
                "score": float(score)
            })

        return results