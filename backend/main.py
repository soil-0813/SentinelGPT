from app.rag.document_loader import DocumentLoader

def main():

    loader = DocumentLoader()

    documents = loader.load_all_documents()

    print(
        f"Loaded {len(documents)} documents"
    )

    print(
        "\nFirst Document:\n"
    )

    print(
        documents[0]
    )


if __name__ == "__main__":
    main()