from app.llm_engine.mitigation_engine import MitigationEngine

def main():

    print("=" * 50)
    print("SentinelGPT Mitigation Engine Test")
    print("=" * 50)

    sample_incident = {
        "attack_type": "Brute Force Attack",
        "severity": "High",
        "failed_logins": 15,
        "successful_login": True
    }

    engine = MitigationEngine()

    mitigation = engine.generate_mitigation(
        sample_incident
    )

    print("\nGenerated Mitigation:\n")

    print(mitigation)


if __name__ == "__main__":
    main()