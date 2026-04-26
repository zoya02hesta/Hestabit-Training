from src.pipelines.image_ingest import ImageIngestor
from src.retriever.image_search import ImageSearch
from src.embeddings.clip_embedder import CLIPEmbedder

# Step 1: Ingest images
ingestor = ImageIngestor()

image_paths = [
    "src/data/images/i1.jpg",
    "src/data/images/i2.png"
]

data = []

for path in image_paths:
    result = ingestor.process_image(path)
    data.append(result)

# Step 2: Search
search = ImageSearch(data)
embedder = CLIPEmbedder()

query = "engineering diagram"

query_embedding = embedder.embed_text(query)

results = search.search_by_text(query_embedding)

print("\n🔹 Search Results:\n")

for r in results:
    print("Image:", r["image_path"])
    print("Caption:", r["caption"])
    print("OCR:", r["ocr_text"])
    print("-" * 40)