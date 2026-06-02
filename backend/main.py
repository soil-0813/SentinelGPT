from app.rag.retriever import Retriever

class DummyEmbedder:

    def embed_text(self, text):
        return [0.1, 0.2, 0.3]


class DummyVectorStore:

    def search(self, embedding, top_k):

        return [
            {
                "source": "mitre_attack.json",
                "content": "MITRE ATT&CK T1110 - Brute Force"
            }
        ]


def main():

    store = DummyVectorStore()

    embedder = DummyEmbedder()

    retriever = Retriever(
        store,
        embedder
    )

    query = input("\nEnter Threat Query: ")

    results = retriever.retrieve(query)

    print("\nResults:\n")

    for result in results:
        print(result)


if __name__ == "__main__":
    main()