from llama_index.core.memory import ChatMemoryBuffer
from llama_index.storage.chat_store.postgres import PostgresChatStore

from src.config.load_config import load_config

config = load_config().postgres_config()
from sqlalchemy import URL, create_engine
from sqlalchemy_utils import create_database, database_exists


def chat_mem(user_id):
    url_object = URL.create(
        "postgresql+psycopg2",
        username=config["user"],
        password=config["pass"],  # plain (unescaped) text
        host=config["host"],
        port=config["port"],
        database=config["db"],
    )
    engine = create_engine(url_object)
    if not database_exists(engine.url):
        create_database(engine.url)

    chat_store = PostgresChatStore.from_params(
        host=config["host"],
        port=config["port"],
        user=config["user"],
        password=config["pass"],
        database=config["db"],
    )

    chat_memory = ChatMemoryBuffer.from_defaults(
        token_limit=5000,
        chat_store=chat_store,
        chat_store_key=user_id,
    )
    return chat_memory
