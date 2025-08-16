from llama_index.embeddings.ollama import OllamaEmbedding

from src.config.load_config import AppConfig

config = AppConfig()


def embedded_model(config: AppConfig = config):
    embedded_config = config.embedded_config()
    base_url = embedded_config["ollama_api"]
    model_name = embedded_config["embedded_model"]

    embedded_model = OllamaEmbedding(model_name=model_name, base_url=base_url)
    return embedded_model
