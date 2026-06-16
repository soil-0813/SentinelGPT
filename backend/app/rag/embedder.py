from sentence_transformers import SentenceTransformer
import numpy as np


class Embedder:

    def __init__(self):

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    def embed_text(self, text):

        return self.model.encode(
            text,
            convert_to_numpy=True
        )

    def embed_documents(self, documents):

        if not documents:
            return np.array([])

        texts = [
            doc.get("content", "")
            for doc in documents
        ]

        return self.model.encode(
            texts,
            convert_to_numpy=True
        )


if __name__ == "__main__":

    print(
        "\nTesting SentinelGPT Embedder...\n"
    )

    embedder = Embedder()

    sample_text = (
        "Brute force attack detected "
        "after multiple failed logins."
    )

    embedding = embedder.embed_text(
        sample_text
    )

    print(
        f"Embedding Shape: {embedding.shape}"
    )

    print(
        "\nFirst 10 Embedding Values:\n"
    )

    print(
        embedding[:10]
    )

    print(
        "\nEmbedder Test Completed Successfully."
    )