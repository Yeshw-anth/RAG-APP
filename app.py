import streamlit as st
import requests

st.set_page_config(
    page_title="Ride App Support Bot",
    layout="centered"
)

st.title("🚕 Ride App Support Chatbot")
st.caption("LLM + RAG (Policy-grounded answers)")

# --- Sidebar for backend selection ---
st.sidebar.title("Settings")
backend_options = ["ollama", "local", "gemini"]
selected_backend = st.sidebar.selectbox("Select LLM Backend:", backend_options)

# --- Session state for chat history ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Chat input ---
user_input = st.chat_input("Ask a question about fares, payments, rides...")

# --- Send message when Enter pressed ---
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    try:
        with st.spinner(f"Thinking with {selected_backend} backend..."):
            response = requests.post(
                "http://localhost:8000/chat",
                json={
                    "message": user_input,
                    "backend": selected_backend
                },
                timeout=15
            )
            answer = response.json().get("answer", "Sorry, no answer.")
            context_used = response.json().get("context_used", [])
    except Exception as e:
        answer = f"Error: {e}"
        context_used = []

    st.session_state.messages.append(
        {"role": "assistant", "content": answer, "context": context_used}
    )

# --- Render chat ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg["role"] == "assistant" and msg.get("context"):
            with st.expander("🔍 Retrieved policy context"):
                for c in msg["context"]:
                    st.markdown(f"- {c}")
 