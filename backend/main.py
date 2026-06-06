from app.rag.document_loader import DocumentLoader


def main():

    loader = DocumentLoader()

    playbooks = loader.load_json(
        "incident_playbooks.json"
    )

    print(
        f"\nLoaded {len(playbooks)} Playbooks\n"
    )

    for playbook in playbooks:

        print(
            f"Playbook: {playbook['incident_type']}"
        )

        print(
            f"Severity: {playbook['severity']}"
        )

        print("-" * 50)


if __name__ == "__main__":
    main()