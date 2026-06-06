from app.rag.document_loader import DocumentLoader


def main():

    loader = DocumentLoader()

    mitre_data = loader.load_json(
        "mitre_attack.json"
    )

    print(
        f"\nLoaded {len(mitre_data)} MITRE Techniques\n"
    )

    for technique in mitre_data:

        print(
            f"{technique['technique_id']} - "
            f"{technique['technique_name']}"
        )

        print(
            f"Tactic: {technique['tactic']}"
        )

        print("-" * 50)


if __name__ == "__main__":
    main()