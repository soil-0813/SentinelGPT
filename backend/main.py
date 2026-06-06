from app.rag.document_loader import DocumentLoader


def main():

    loader = DocumentLoader()

    owasp_data = loader.load_json(
        "owasp_top10.json"
    )

    print(
        f"\nLoaded {len(owasp_data)} OWASP Entries\n"
    )

    for item in owasp_data:

        print(
            f"{item['id']} - {item['name']}"
        )

        print(
            f"Severity: {item['severity']}"
        )

        print("-" * 50)


if __name__ == "__main__":
    main()