import pandas as pd
from llama_index.core import Document
from llama_index.core.node_parser import SentenceSplitter


class Process_doc:
    def __init__(
        self, file_path: str = None, chunk_size: int = 1024, chunk_overlap: int = 200
    ):
        self.path = file_path
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def csv_to_doc(self, file_path=None):
        path = file_path or self.path
        df = pd.read_csv(path)
        records = df.to_dict(orient="records")
        documents = [
            Document(
                text=str(t),
                metadata={
                    "Genre": t["Genre"],
                    "Director": t["Director"],
                    "Released_Year": t["Released_Year"],
                },
            )
            for t in records
        ]
        return documents

    def parser(self):

        node_parser = SentenceSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
        )
        return node_parser

    def run(self, documents: list[Document] = None):
        documents = documents or self.csv_to_doc(self.path)
        parser = self.parser()
        nodes = parser.get_nodes_from_documents(documents)
        return nodes


if __name__ == "__main__":
    PATH = "src/data/imdb_top_1000.csv"
    pipe = Process_doc(file_path=PATH)
    nodes = pipe.run()
    print(nodes)
