from app.llm_engine.explainability import explain_with_ollama


def main():

    print("=" * 50)
    print("SentinelGPT Explainability Test")
    print("=" * 50)

    sample_incident = {
        "attack_type": "Brute Force Attack",
        "severity": "High",
        "failed_logins": 15,
        "successful_login": True,
        "source_ip": "192.168.1.100",
        "mitre_technique": "T1110"
    }

    print("\nSending incident to Ollama...\n")

    explanation = explain_with_ollama(
        sample_incident
    )

    print("\nGenerated Explanation:\n")

    print(explanation)


if __name__ == "__main__":
    main()