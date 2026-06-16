import uuid
from datetime import datetime


def generate_incident_id():
    """
    Generate unique incident IDs.
    """

    return f"INC-{uuid.uuid4().hex[:8].upper()}"


def current_timestamp():
    """
    Return current UTC timestamp.
    """

    return datetime.utcnow().isoformat()


def severity_to_score(
    severity: str
):

    severity = severity.lower()

    mapping = {
        "low": 25,
        "medium": 50,
        "high": 75,
        "critical": 95
    }

    return mapping.get(severity, 0)


def print_incident(
    incident: dict
):

    print("\n========== INCIDENT ==========\n")

    for key, value in incident.items():
        print(f"{key}: {value}")

    print("\n==============================\n")