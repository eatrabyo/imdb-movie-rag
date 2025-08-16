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
        self.postgres_host = os.getenv("POSTGRES_HOST")
        self.postgres_port = os.getenv("POSTGRES_port")
        self.postgres_db = os.getenv("POSTGRES_DB")
        self.postgres_user = os.getenv("POSTGRES_USER")
        self.postgres_pass = os.getenv("POSTGRES_PASSWORD")

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

    def postgres_config(self):
        config = {
            "host": self.postgres_host,
            "port": self.postgres_port,
            "user": self.postgres_user,
            "pass": self.postgres_pass,
            "db": self.postgres_db,
        }
        return config


def load_config():
    config = AppConfig()
    return config
