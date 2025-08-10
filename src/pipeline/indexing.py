from llama_index.core import StorageContext, VectorStoreIndex
from llama_index.core.schema import Node
from llama_index.core.vector_stores.types import BasePydanticVectorStore
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

from src.embedding.embedded_model import embedded_model


class Indexer:
    def __init__(
        self,
        vector_store: BasePydanticVectorStore = None,
        indexer_config: dict = None,
    ):
        self.embed_model = embedded_model()
        self.qdrant_client = QdrantClient(indexer_config["vector_db"])
        self.collection_name = indexer_config["collection_name"]
        self.vector_store = vector_store or self.load_qdrant()
        self.index = self.load_index_from_vector_store(
            self.vector_store, self.embed_model
        )

    def get_index(self):
        return self.index

    def load_qdrant(self):
        vector_store = QdrantVectorStore(
            client=self.qdrant_client,
            collection_name=self.collection_name,
        )
        return vector_store

    def check_collection_exists(self, **kwargs):
        collection_name = kwargs.get("collection_name", self.collection_name)
        result = self.qdrant_client.collection_exists(collection_name=collection_name)
        if result:
            print(f"collection: {collection_name} is already exists")
        else:
            print(f"collection: {collection_name} is not exists")
        return result

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

    def retrieve(self, query: str, top_k=5):
        return self.index.as_retriever(similarity_top_k=top_k).retrieve(query)
