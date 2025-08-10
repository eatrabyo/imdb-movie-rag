import os

from dotenv import find_dotenv, load_dotenv

from src.config.chat_engine_config import ChatEngineConfig

load_dotenv(find_dotenv())


class AppConfig:
    def __init__(self):
        self.ollama_url = os.getenv("OLLAMA_API")
        self.vector_db_url = os.getenv("QDRANT_URL", "http://localhost:6333")
        self.collection = os.getenv("COLLECTION_NAME")
        self.embedded_model = os.getenv("EMBEDDED_MODEL")

    def indexer_config(self):
        config = {
            "vector_db": self.vector_db_url,
            "collection_name": self.collection,
        }
        return config

    def embedded_config(self):
        config = {
            "embedded_model": self.embedded_model,
            "ollama_api": self.ollama_url,
        }
        return config
