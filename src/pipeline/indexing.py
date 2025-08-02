import os

from dotenv import find_dotenv, load_dotenv
from llama_index.core import StorageContext, VectorStoreIndex
from llama_index.core.base.embeddings.base import BaseEmbedding
from llama_index.core.schema import Node
from llama_index.core.vector_stores.types import BasePydanticVectorStore
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

from src.embedding.embedded_model import embedded_model


class Indexer:
    def __init__(
        self,
        embed_model: BaseEmbedding = None,
        vector_store: BasePydanticVectorStore = None,
        db_config: dict = None,
        ollama_url: str = None,
    ):
        self.embed_model = embedded_model(ollama_url)
        self.vector_store = vector_store or self.load_qdrant(db_config)
        self.index = self.load_index_from_vector_store(
            self.vector_store, self.embed_model
        )

    def get_index(self):
        return self.index

    def load_qdrant(self, db_config):

        client = QdrantClient(db_config["database"])
        vector_store = QdrantVectorStore(
            client=client, collection_name=db_config["collection_name"]
        )
        return vector_store

    def load_index_from_vector_store(self, vector_store, embed_model):
        """
        Loads an index from a given vector store using the specified embedding model.

        Args:
            vector_store: The vector store from which to load the index.
            embed_model: The embedding model to use for loading the index.

        Returns:
            The loaded index.
        """
        self.index = VectorStoreIndex.from_vector_store(
            vector_store=vector_store, embed_model=embed_model
        )
        return self.index

    def add_nodes_to_index(self, nodes: list[Node], **kwargs):
        self.index.insert_nodes(nodes, **kwargs)

    def remove_nodes_from_index(self, node_ids, **kwargs):
        self.index.delete_nodes(node_ids, **kwargs)

    def retrive(self, query: str, top_k=5):
        return self.index.as_retriever(similarity_top_k=top_k).retrieve(query)

    def _get_default_embed_model(self, base_url=None):
        base_url = base_url or os.getenv("ollama_api", "http://localhost:11434")
        embed_model = OllamaEmbedding(model_name="bge-m3", base_url=base_url)
        return embed_model


if __name__ == "__main__":
    load_dotenv(find_dotenv())

    config = {
        "database": os.getenv("qdrant_url", "http://localhost:6333"),
        "collection_name": "test",
    }
    indexer = Indexer(db_config=config, ollama_url=os.getenv("ollama_api"))
    nodes = indexer.retrive("How to open a bank account?")
    for node in nodes:
        print("Node ID:", node.node_id)
        print("Node Text:", node.text[:100] + "...")
        print("=====================================")
