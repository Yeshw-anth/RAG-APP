# llm.py
import os
from config import LLM_BACKEND, LOCAL_MODEL_PATH, GEMINI_MODEL, GEMINI_API_KEY
import ollama
from llama_cpp import Llama
from google import genai
from google.genai import types

llm = None

# -----------------------------
def generate(prompt: str, backend: str = None) -> str:
    """
    Generate response using the selected backend.
    If no backend is provided, uses the default from config.py
    """
    backend = backend or LLM_BACKEND

    # 1️⃣ Ollama
    if backend == "ollama":
        try:
            client = ollama.Client()
        except ImportError:
            raise ImportError("Ollama not installed. Install with 'pip install ollama'")
        if not client:
            raise RuntimeError("Ollama client not initialized")
        messages = [
            {"role": "system", "content": "You are a ride-app support assistant. provide clear and formal answers easy to understand."},
            {"role": "user", "content": prompt}
        ]
        resp = client.chat(model="phi3:mini", messages=messages)
        if isinstance(resp, dict):
            if "message" in resp and isinstance(resp["message"], dict) and "content" in resp["message"]:
                return resp["message"]["content"].strip()
            elif "text" in resp:
                return resp["text"].strip()
        return str(resp)

    # 2️⃣ Local llama_cpp
    elif backend == "local":
        try:
            if not os.path.exists(LOCAL_MODEL_PATH):
                raise FileNotFoundError(f"Local model not found at {LOCAL_MODEL_PATH}")
            llm = Llama(model_path=LOCAL_MODEL_PATH, n_ctx=2048, n_threads=8)
        except ImportError:
            raise ImportError("llama_cpp not installed. Install with 'pip install llama_cpp'")
        if not llm:
            raise RuntimeError("Local llama_cpp model not loaded")
        out = llm(prompt, max_tokens=300, temperature=0.2, stop=["</s>"])
        # llama_cpp uses 'choices' list
        return out["choices"][0]["text"].strip()

    # 3️⃣ Gemini
    elif backend == "gemini":
        try:
            # Initialize client with API key
            gem_client = genai.Client(api_key=GEMINI_API_KEY)
        except ImportError:
            raise ImportError("Install Google GenAI SDK: pip install google-genai")
        if not gem_client:
            raise RuntimeError("Gemini client not initialized")

        # Gemini expects a STRING, not chat messages
        full_prompt = (
            "You are a ride-app support assistant.\n\n"
            f"{prompt}"
        )

        response = gem_client.models.generate_content(
            model=GEMINI_MODEL,
            contents=full_prompt,   # ✅ STRING ONLY
        )

        return response.text.strip()
