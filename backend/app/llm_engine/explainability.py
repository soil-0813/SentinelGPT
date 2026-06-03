import requests


def explain_with_ollama(incident_data):

    prompt = f"""
    You are a SOC analyst.

    Explain this incident:

    {incident_data}

    Provide:
    1. Attack Summary
    2. Reasoning Steps
    3. Alternative Hypotheses
    4. Severity Justification
    5. Recommended Actions
    """

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )

    data = response.json()

    print("Ollama Response:")
    print(data)

    return data.get(
        "response",
        "No response returned from Ollama."
    )