from llama_index.core.chat_engine import ContextChatEngine

from src.config.load_config import load_config
from src.core.chat_store import chat_mem
from src.core.indexing import Indexer
from src.core.llm_model import llm_model
from src.utils.prompt_instruction import prompt_template

config = load_config()


indexer = Indexer(indexer_config=config.indexer_config()).get_index()


def chat_engine(user_id):

    chat_engine = ContextChatEngine(
        retriever=indexer.as_retriever(),
        llm=llm_model(),
        memory=chat_mem(user_id),
        prefix_messages=[],
        context_template=prompt_template,
    )
    return chat_engine
