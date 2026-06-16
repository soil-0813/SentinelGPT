from typing import List, Dict


class Retriever:
    """
    Retrieves the most relevant documents
    from the SentinelGPT vector store.
    """

    def __init__(self, vector_store, embedder):

        self.vector_store = vector_store
        self.embedder = embedder

    def retrieve(
        self,
        query: str,
        top_k: int = 5
    ) -> List[Dict]:

        query_embedding = self.embedder.embed_text(
            query
        )

        results = self.vector_store.search(
            query_embedding,
            top_k
        )

        return results


if __name__ == "__main__":

    print(
        "\nRetriever module loaded successfully."
    )

    print(
        "Use this module together with "
        "Embedder and VectorStore."
    )