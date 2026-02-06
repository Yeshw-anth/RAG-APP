# server.py
from fastapi import FastAPI
from pydantic import BaseModel
from ingest import run_ingestion
from llm import generate
from rag import retrieve
from prompts import build_prompt  # your RAG functions

app = FastAPI()

@app.on_event("startup")
def startup_event():
    run_ingestion()   # 🔥 ALWAYS run

class ChatRequest(BaseModel):
    message: str
    backend: str # optional override

@app.post("/chat")
def chat(req: ChatRequest):
    # 1️⃣ Retrieve relevant chunks from FAISS
    chunks = retrieve(req.message)  # returns list of text chunks
    context = "\n".join(chunks)

    # 2️⃣ Build prompt including retrieved context
    prompt = build_prompt(req.message, context)

    # 3️⃣ Generate response using selected LLM
    answer = generate(prompt,backend=req.backend)

    # 4️⃣ Return answer along with which context was used
    return {
        "context_used": chunks,
        "answer": answer
    }
