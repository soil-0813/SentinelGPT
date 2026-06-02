from app.rag.embedder import Embedder


def main():

    print("=" * 50)
    print("SentinelGPT Embedder Test")
    print("=" * 50)

    embedder = Embedder()

    sample_text = (
        "Brute force attack detected after "
        "multiple failed login attempts."
    )

    print("\nGenerating embedding...\n")

    embedding = embedder.embed_text(
        sample_text
    )

    print(
        f"Embedding Dimension: {len(embedding)}"
    )

    print(
        f"Embedding Shape: {embedding.shape}"
    )

    print(
        "\nFirst 10 Values:\n"
    )

    print(
        embedding[:10]
    )

    print(
        "\nEmbedder Test Completed Successfully."
    )


if __name__ == "__main__":
    main()