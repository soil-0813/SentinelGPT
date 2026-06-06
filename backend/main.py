from app.data_sources.log_loader import load_all_logs

from app.preprocessing.parser import parse_logs
from app.preprocessing.cleaner import clean_logs
from app.preprocessing.log_normalizer import normalize_logs
from app.preprocessing.feature_extractor import extract_features

from app.correlation.event_correlator import correlate_events
from app.correlation.timeline_builder import build_timeline
from app.correlation.severity_scorer import score_attack


def main():

    print("\n========== SENTINELGPT PIPELINE TEST ==========\n")

    # ----------------------------------
    # Load Logs
    # ----------------------------------
    raw_logs = load_all_logs()
    print(f"Raw logs loaded: {len(raw_logs)}")

    # ----------------------------------
    # Parse Logs
    # ----------------------------------
    parsed_logs = parse_logs(raw_logs)
    print(f"Parsed logs: {len(parsed_logs)}")

    # ----------------------------------
    # Clean Logs
    # ----------------------------------
    cleaned_logs = clean_logs(parsed_logs)
    print(f"Cleaned logs: {len(cleaned_logs)}")

    # ----------------------------------
    # Normalize Logs
    # ----------------------------------
    normalized_logs = normalize_logs(cleaned_logs)
    print(f"Normalized logs: {len(normalized_logs)}")

    # ----------------------------------
    # Extract Features
    # ----------------------------------
    feature_logs = extract_features(normalized_logs)
    print(f"Feature enriched logs: {len(feature_logs)}")

    # ----------------------------------
    # Correlate Events
    # ----------------------------------
    attack_stories = correlate_events(feature_logs)
    print(f"Attack stories detected: {len(attack_stories)}")

    if not attack_stories:
        print("\nNo correlated attacks detected.\n")
        return

    print("\n========== CORRELATION RESULTS ==========\n")

    for idx, story in enumerate(attack_stories, start=1):

        print(f"\nATTACK #{idx}")
        print("-" * 60)

        print(f"Attack Type : {story['attack_type']}")
        print(f"Source IP   : {story['source_ip']}")
        print(f"Confidence  : {story['confidence']}")

        print("\nReasoning:")

        for step in story["reasoning"]:
            print(f"  - {step}")

        # ----------------------------------
        # Build Timeline
        # ----------------------------------
        timeline = build_timeline(story)

        print("\nTimeline:")

        for event in timeline:
            print(
                f"  [{event['timestamp']}] "
                f"{event['event_type']} "
                f"({event['source']})"
            )

        # ----------------------------------
        # Severity Scoring
        # ----------------------------------
        severity_data = score_attack(story)

        print("\nRisk Assessment")

        print(
            f"Risk Score : {severity_data['risk_score']}"
        )

        print(
            f"Severity   : {severity_data['severity']}"
        )

        print("\nJustification:")

        for reason in severity_data["justification"]:
            print(f"  - {reason}")

        print("\nSupporting Events:")

        print(
            f"Total correlated logs: "
            f"{len(story['supporting_logs'])}"
        )

        print("-" * 60)

    print("\n========== PIPELINE SUCCESS ==========\n")


if __name__ == "__main__":
    main()