# ingest.py
from sentence_transformers import SentenceTransformer
import faiss
import os
import pickle

def run_ingestion():
    print("🔄 Running ingestion...")

    model = SentenceTransformer("all-MiniLM-L6-v2")

    docs = open("data/fare_policy.txt", encoding="utf-8").read().split("\n")
    embeddings = model.encode(docs, normalize_embeddings=True)

    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)

    os.makedirs("index", exist_ok=True)
    faiss.write_index(index, "index/faiss.index")

    with open("index/docs.pkl", "wb") as f:
        pickle.dump(docs, f)

    print("✅ Index rebuilt")
