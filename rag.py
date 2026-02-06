import faiss, pickle
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

index = faiss.read_index("index/faiss.index")
docs = pickle.load(open("index/docs.pkl", "rb"))

def retrieve(query, k=3):
    q_emb = model.encode([query], normalize_embeddings=True)
    scores, idxs = index.search(q_emb, k)

    return [docs[i] for i in idxs[0]]
