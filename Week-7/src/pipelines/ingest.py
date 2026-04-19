import os
from tqdm import tqdm

from src.utils.loader import load_file
from src.utils.cleaner import clean_text
from src.utils.chunker import chunk_text
from src.embeddings.embedder import Embedder
from src.vectorstore.faiss_store import FaissStore

DATA_PATH = "src/data/raw"

def run_ingestion():
    embedder = Embedder()

    all_chunks = []

    for file in tqdm(os.listdir(DATA_PATH)):
        path = os.path.join(DATA_PATH, file)

        
        if os.path.isdir(path):
            print(f"Skipping folder: {file}")
            continue

        
        if not file.endswith((".txt", ".pdf", ".docx", ".csv")):
            print(f"Skipping unsupported file: {file}")
            continue

        text = load_file(path)
        text = clean_text(text)

        if not text.strip():
            print(f"No text extracted from: {file}")
            continue

        chunks = chunk_text(text)

        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "text": chunk,
                "source": file,
                "chunk_id": i
                })

    print("Total chunks:", len(all_chunks))

    embeddings = embedder.embed(all_chunks)

    dim = len(embeddings[0])
    store = FaissStore(dim)

    store.add(embeddings, all_chunks)
    store.save()

    print("✅ Ingestion complete")

if __name__ == "__main__":
    run_ingestion()