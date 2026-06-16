import requests


class MitigationEngine:

    def __init__(
        self,
        model="llama3"
    ):

        self.model = model

    def generate_mitigation(
        self,
        incident_data
    ):

        prompt = f"""
        You are a Senior SOC Analyst.

        Analyze the following security incident:

        {incident_data}

        Provide:

        1. Immediate Containment Actions
        2. Investigation Steps
        3. Eradication Steps
        4. Recovery Steps
        5. Long-Term Security Improvements
        6. Recommended MITRE ATT&CK Mitigations

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
            "No mitigation generated."
        )


if __name__ == "__main__":

    sample_incident = {
        "attack_type": "Brute Force Attack",
        "severity": "High",
        "failed_logins": 15,
        "successful_login": True,
        "source_ip": "192.168.1.100"
    }

    engine = MitigationEngine()

    result = engine.generate_mitigation(
        sample_incident
    )

    print("\nMitigation Plan:\n")

    print(result)