from llama_index.llms.ollama import Ollama
from src.config.load_config import load_config

config = load_config()


def llm_model(llm_config=config.llm_config()):
    llm = Ollama(
        model=llm_config["llm_model"],
        temperature=0.2,
        base_url=llm_config["ollama_api"],
        request_timeout=600,
        stream=True,
    )
    return llm
