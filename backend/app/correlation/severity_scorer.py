import logging

logger = logging.getLogger(__name__)


def score_attack(story):

    attack_type = story["attack_type"]

    score = 50
    reasons = []

    if attack_type == "Brute Force Attack":

        score = 85

        reasons.append(
            "Repeated authentication failures observed."
        )

        reasons.append(
            "Successful login after failures."
        )

    elif attack_type == "Credential Phishing":

        score = 90

        reasons.append(
            "Credential theft indicators present."
        )

        reasons.append(
            "Suspicious authentication activity."
        )

    elif attack_type == "Ransomware":

        score = 98

        reasons.append(
            "Malware execution detected."
        )

        reasons.append(
            "Encryption activity detected."
        )

    severity = calculate_severity(score)

    return {
        "risk_score": score,
        "severity": severity,
        "justification": reasons
    }


def calculate_severity(score):

    if score >= 95:
        return "critical"

    if score >= 80:
        return "high"

    if score >= 60:
        return "medium"

    return "low"