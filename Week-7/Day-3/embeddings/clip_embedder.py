from PIL import Image
from sentence_transformers import SentenceTransformer

class CLIPEmbedder:
    def __init__(self):
        self.model = SentenceTransformer('clip-ViT-B-32')

    def embed_image(self, image_path):
        image = Image.open(image_path)
        embedding = self.model.encode(image)
        return embedding

    def embed_text(self, text):
        return self.model.encode(text)