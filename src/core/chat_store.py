from llama_index.core.memory import ChatMemoryBuffer
from llama_index.storage.chat_store.postgres import PostgresChatStore

from src.config.load_config import load_config

config = load_config()


def chat_mem(user_id):
    chat_store = PostgresChatStore.from_params(
        host=config["pg_vector_host"],
        port=config["pg_vector_port"],
        user=config["pg_vector_user"],
        password=config["pg_vector_pass"],
        database=config["db"],
        table_name="chat_history",
    )

    chat_memory = ChatMemoryBuffer.from_defaults(
        token_limit=5000,
        chat_store=chat_store,
        chat_store_key=user_id,
    )
    return chat_memory
