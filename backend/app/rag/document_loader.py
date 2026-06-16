import json
from pathlib import Path
from typing import List, Dict


class DocumentLoader:
    """
    Loads cybersecurity threat intelligence documents
    from the SentinelGPT knowledge base.
    """

    def __init__(self):

        self.base_path = Path(
            "datasets/threat_intelligence"
        )

    def load_json(self, filename: str) -> List[Dict]:

        file_path = self.base_path / filename

        try:

            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as file:

                return json.load(file)

        except FileNotFoundError:

            print(
                f"File not found: {file_path}"
            )

            return []

        except Exception as e:

            print(
                f"Error loading {filename}: {e}"
            )

            return []

    def load_all_documents(self) -> List[Dict]:

        documents = []

        files = [
            "mitre_attack.json",
            "cve_database.json",
            "owasp_top10.json",
            "incident_playbooks.json"
        ]

        for filename in files:

            data = self.load_json(filename)

            for item in data:

                documents.append(
                    {
                        "source": filename,
                        "content": json.dumps(
                            item,
                            ensure_ascii=False
                        )
                    }
                )

        return documents


if __name__ == "__main__":

    loader = DocumentLoader()

    documents = loader.load_all_documents()

    print(
        f"\nLoaded {len(documents)} documents\n"
    )

    if documents:

        print("First Document:\n")

        print(documents[0])