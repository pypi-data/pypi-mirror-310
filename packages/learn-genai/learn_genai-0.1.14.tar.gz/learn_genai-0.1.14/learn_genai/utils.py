import subprocess
import time
import streamlit as st

def ensure_ollama_service():
    try:
        subprocess.run(["ollama", "serve"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        st.error("Ollama service is not running. Please start the Ollama service and try again.")
        st.stop()

def ensure_ollama_models():
    models = ["llama2:3b", "nomic-embed-text:latest"]
    for model in models:
        try:
            subprocess.run(["ollama", "pull", model], check=True)
        except subprocess.CalledProcessError:
            st.error(f"Failed to pull {model}. Please ensure Ollama is installed and running.")
            time.sleep(2)
            st.stop()
