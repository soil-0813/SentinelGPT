import faiss
import numpy as np


class VectorStore:
    """
    FAISS-based vector store for SentinelGPT.
    Stores document embeddings and performs similarity search.
    """

    def __init__(self):

        self.index = None
        self.documents = []

    def build_index(
        self,
        embeddings,
        documents
    ):

        embeddings = np.array(
            embeddings,
            dtype=np.float32
        )

        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatL2(
            dimension
        )

        self.index.add(
            embeddings
        )

        self.documents = documents

    def search(
        self,
        query_embedding,
        top_k=5
    ):

        if self.index is None:

            return []

        query_embedding = np.array(
            [query_embedding],
            dtype=np.float32
        )

        distances, indices = self.index.search(
            query_embedding,
            top_k
        )

        results = []

        for idx in indices[0]:

            if idx < len(self.documents):

                results.append(
                    self.documents[idx]
                )

        return results


if __name__ == "__main__":

    print(
        "VectorStore module loaded successfully."
    )

    print(
        "Run with Embedder and Retriever for testing."
    )