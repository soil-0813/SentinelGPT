import requests


class ThreatAnalyzer:

    def __init__(
        self,
        model="llama3"
    ):

        self.model = model

    def analyze_threat(
        self,
        incident_data,
        retrieved_context=""
    ):

        prompt = f"""
        You are a Senior SOC Analyst.

        Incident Data:
        {incident_data}

        Threat Intelligence Context:
        {retrieved_context}

        Perform the following:

        1. Identify the likely attack type
        2. Explain the attack step-by-step
        3. Map to MITRE ATT&CK techniques
        4. Assign a severity level
        5. Justify the severity
        6. Suggest immediate response actions
        7. Generate an executive summary

        Format the response clearly.
        """

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            }
        )

        data = response.json()

        return data.get(
            "response",
            "No threat analysis generated."
        )


if __name__ == "__main__":

    sample_incident = {
        "attack_type": "Brute Force Attack",
        "failed_logins": 15,
        "successful_login": True,
        "source_ip": "192.168.1.100"
    }

    analyzer = ThreatAnalyzer()

    result = analyzer.analyze_threat(
        sample_incident
    )

    print("\nThreat Analysis:\n")

    print(result)