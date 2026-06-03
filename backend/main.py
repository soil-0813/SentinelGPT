from app.llm_engine.threat_analyzer import ThreatAnalyzer

def main():

    print("=" * 50)
    print("SentinelGPT Threat Analyzer Test")
    print("=" * 50)

    sample_incident = {
        "attack_type": "Brute Force Attack",
        "severity": "High",
        "failed_logins": 15,
        "successful_login": True,
        "source_ip": "192.168.1.100"
    }

    analyzer = ThreatAnalyzer()

    analysis = analyzer.analyze_threat(
        sample_incident
    )

    print("\nGenerated Analysis:\n")

    print(analysis)


if __name__ == "__main__":
    main()