import pytesseract
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

from src.embeddings.clip_embedder import CLIPEmbedder


class ImageIngestor:
    def __init__(self):
        self.embedder = CLIPEmbedder()

        self.processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        self.model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

    def extract_text(self, image_path):
        image = Image.open(image_path)
        return pytesseract.image_to_string(image)

    def generate_caption(self, image_path):
        image = Image.open(image_path).convert('RGB')

        inputs = self.processor(image, return_tensors="pt")
        output = self.model.generate(**inputs)

        caption = self.processor.decode(output[0], skip_special_tokens=True)
        return caption

    def process_image(self, image_path):
        ocr_text = self.extract_text(image_path)
        caption = self.generate_caption(image_path)
        embedding = self.embedder.embed_image(image_path)

        return {
            "image_path": image_path,
            "ocr_text": ocr_text,
            "caption": caption,
            "embedding": embedding
        }