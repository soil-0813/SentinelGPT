import logging
from collections import defaultdict

logger = logging.getLogger(__name__)


def correlate_events(feature_logs):
    """
    Correlates logs into attack stories.
    """

    if not feature_logs:
        return []

    grouped_by_ip = defaultdict(list)

    for log in feature_logs:

        source_ip = log["log_features"].get("source_ip", "unknown")

        if source_ip:
            grouped_by_ip[source_ip].append(log)

    attack_stories = []

    for ip, logs in grouped_by_ip.items():

        story = detect_attack_pattern(ip, logs)

        if story:
            attack_stories.append(story)

    logger.info(
        f"Generated {len(attack_stories)} correlated attack stories"
    )

    return attack_stories


def detect_attack_pattern(source_ip, logs):

    failed_logins = 0
    successful_logins = 0
    malware_events = 0
    phishing_events = 0
    ransomware_events = 0

    reasoning = []

    for log in logs:

        features = log["log_features"]

        if features["is_failed_login"]:
            failed_logins += 1

        if features["is_successful_login"]:
            successful_logins += 1

        if features["is_malware"]:
            malware_events += 1

        if features["is_phishing"]:
            phishing_events += 1

        if features["is_ransomware"]:
            ransomware_events += 1

    # Brute Force

    if failed_logins >= 5 and successful_logins >= 1:

        reasoning.append(
            f"{failed_logins} failed login attempts observed."
        )

        reasoning.append(
            "Successful login occurred after repeated failures."
        )

        reasoning.append(
            "Possible credential compromise detected."
        )

        return {
            "attack_type": "Brute Force Attack",
            "source_ip": source_ip,
            "confidence": 0.92,
            "reasoning": reasoning,
            "supporting_logs": logs
        }

    # Phishing

    if phishing_events >= 1 and successful_logins >= 1:

        reasoning.append(
            "Phishing indicators detected."
        )

        reasoning.append(
            "User authentication occurred afterward."
        )

        reasoning.append(
            "Potential credential theft."
        )

        return {
            "attack_type": "Credential Phishing",
            "source_ip": source_ip,
            "confidence": 0.94,
            "reasoning": reasoning,
            "supporting_logs": logs
        }

    # Ransomware

    if malware_events >= 1 and ransomware_events >= 1:

        reasoning.append(
            "Malware execution detected."
        )

        reasoning.append(
            "Ransomware indicators observed."
        )

        reasoning.append(
            "Likely encryption activity."
        )

        return {
            "attack_type": "Ransomware",
            "source_ip": source_ip,
            "confidence": 0.98,
            "reasoning": reasoning,
            "supporting_logs": logs
        }

    return None