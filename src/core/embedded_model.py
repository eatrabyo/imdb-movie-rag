import json
import logging

import requests
from llama_index.embeddings.ollama import OllamaEmbedding

from src.config.load_config import AppConfig, load_config

config = load_config()
logger = logging.getLogger(__name__)


def embedded_model(config: AppConfig = config):
    embedded_config = config.embedded_config()
    base_url = embedded_config["ollama_api"]
    model_name = embedded_config["embedded_model"]
    data = {"model": model_name}
    response = requests.post(f"{base_url}/api/pull", data=json.dumps(data))

    if response.status_code == 200:
        logger.info(f"Pulled model {model_name} from {base_url}")
    else:
        logger.error(f"{response.status_code}: {response.text}")

    embedded_model = OllamaEmbedding(model_name=model_name, base_url=base_url)
    return embedded_model
