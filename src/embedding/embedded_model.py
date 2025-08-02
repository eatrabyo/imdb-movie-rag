import os

from llama_index.embeddings.ollama import OllamaEmbedding


def embedded_model(base_url):
    base_url = base_url or os.getenv("ollama_api", "http://localhost:11434")
    embedded_model = OllamaEmbedding(
        model_name=os.getenv("embedded_model"), base_url=base_url
    )
    return embedded_model
