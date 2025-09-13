import json
import logging

import requests
from llama_index.llms.ollama import Ollama

from src.config.load_config import load_config

logger = logging.getLogger(__name__)
config = load_config()


def llm_model(llm_config=config.llm_config()):

    base_url = llm_config["ollama_api"]
    model_name = llm_config["llm_model"]
    data = {"model": model_name}
    response = requests.post(f"{base_url}/api/pull", data=json.dumps(data))

    if response.status_code == 200:
        logger.info(f"Pulled model {model_name} from {base_url}")
    else:
        logger.error(f"{response.status_code}: {response.text}")

    llm = Ollama(
        model=llm_config["llm_model"],
        temperature=0.2,
        base_url=llm_config["ollama_api"],
        request_timeout=600,
        stream=True,
    )
    return llm
