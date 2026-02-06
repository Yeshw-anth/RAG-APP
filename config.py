# config.py

# Backend selection: "ollama", "local", or "gemini"
LLM_BACKEND = "gemini"

# Local model path (for llama_cpp / GGUF models)
LOCAL_MODEL_PATH = "models\mpt-3b-8k-instruct.q4_k_m.gguf"

# Gemini 2.5 Flash configuration
GEMINI_MODEL = "gemini-2.5-flash"  # fixed model name
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"  # or use environment variable
