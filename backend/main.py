from app.rag.document_loader import DocumentLoader


def main():

    print("=" * 50)
    print("SentinelGPT RAG Document Loader Test")
    print("=" * 50)

    loader = DocumentLoader()

    documents = loader.load_all_documents()

    print(f"\nLoaded Documents: {len(documents)}")

    if len(documents) > 0:

        print("\nFirst Document:")
        print("-" * 50)
        print(documents[0])

    else:

        print("\nNo documents found.")

    print("\nTest Completed Successfully")


if __name__ == "__main__":
    main()