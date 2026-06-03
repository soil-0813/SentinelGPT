from app.llm_engine.vulnerability_reasoner import VulnerabilityReasoner

def main():

    print("=" * 50)
    print("SentinelGPT Vulnerability Reasoner Test")
    print("=" * 50)

    vulnerability = {
        "cve_id": "CVE-2021-44228",
        "name": "Log4Shell",
        "cvss_score": 10.0
    }

    reasoner = VulnerabilityReasoner()

    analysis = reasoner.analyze_vulnerability(
        vulnerability
    )

    print("\nGenerated Analysis:\n")

    print(analysis)


if __name__ == "__main__":
    main()