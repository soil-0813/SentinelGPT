import uuid

from app.data_sources.log_loader import load_all_logs

from app.preprocessing.parser import parse_logs
from app.preprocessing.cleaner import clean_logs
from app.preprocessing.log_normalizer import normalize_logs

from app.preprocessing.feature_extractor import extract_features

from app.correlation.event_correlator import correlate_events

from app.correlation.timeline_builder import build_timeline
from app.correlation.severity_scorer import score_attack

from app.database.db import (
    initialize_database,
    save_incident,
    get_all_incidents
)

def main():

    print("\n========== SENTINELGPT PIPELINE TEST ==========\n")

    # ==================================================
    # DATABASE INITIALIZATION
    # ==================================================

    initialize_database()

    # ==================================================
    # LOAD LOGS
    # ==================================================

    raw_logs = load_all_logs()

    print(f"Raw logs loaded: {len(raw_logs)}")

    # ==================================================
    # PARSE LOGS
    # ==================================================

    parsed_logs = parse_logs(raw_logs)

    print(f"Parsed logs: {len(parsed_logs)}")

    # ==================================================
    # CLEAN LOGS
    # ==================================================

    cleaned_logs = clean_logs(parsed_logs)

    print(f"Cleaned logs: {len(cleaned_logs)}")

    # ==================================================
    # NORMALIZE LOGS
    # ==================================================

    normalized_logs = normalize_logs(cleaned_logs)

    print(f"Normalized logs: {len(normalized_logs)}")

    # ==================================================
    # FEATURE EXTRACTION
    # ==================================================

    feature_logs = extract_features(normalized_logs)

    print(f"Feature enriched logs: {len(feature_logs)}")

    # ==================================================
    # CORRELATION ENGINE
    # ==================================================

    attack_stories = correlate_events(feature_logs)

    print(f"Attack stories detected: {len(attack_stories)}")

    if not attack_stories:

        print("\nNo correlated attacks detected.\n")
        return

    print("\n========== CORRELATION RESULTS ==========\n")

    # ==================================================
    # PROCESS ATTACK STORIES
    # ==================================================

    for idx, story in enumerate(attack_stories, start=1):

        print(f"\nATTACK #{idx}")
        print("-" * 60)

        print(f"Attack Type : {story['attack_type']}")
        print(f"Source IP   : {story['source_ip']}")
        print(f"Confidence  : {story['confidence']}")

        print("\nReasoning:")

        for step in story["reasoning"]:
            print(f"  - {step}")

        # --------------------------------------------
        # Timeline
        # --------------------------------------------

        timeline = build_timeline(story)

        print("\nTimeline:")

        for event in timeline:

            print(
                f"  [{event['timestamp']}] "
                f"{event['event_type']} "
                f"({event['source']})"
            )

        # --------------------------------------------
        # Severity Scoring
        # --------------------------------------------

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

        # --------------------------------------------
        # Incident Object
        # --------------------------------------------

        incident = {

            "incident_id":
                str(uuid.uuid4()),

            "attack_type":
                story["attack_type"],

            "severity":
                severity_data["severity"],

            "risk_score":
                severity_data["risk_score"],

            "source_ip":
                story["source_ip"],

            "confidence":
                story["confidence"],

            "reasoning":
                story["reasoning"],

            "timeline":
                timeline
        }

        save_incident(incident)

        print("\nIncident saved to database.")

        print(
            f"Total correlated logs: "
            f"{len(story['supporting_logs'])}"
        )

        print("-" * 60)

    # ==================================================
    # VERIFY DATABASE
    # ==================================================

    print("\n========== DATABASE CONTENT ==========\n")

    incidents = get_all_incidents()

    print(
        f"Incidents stored in database: "
        f"{len(incidents)}"
    )

    for incident in incidents:

        print(
            f"ID={incident[0]} | "
            f"Attack={incident[1]} | "
            f"Severity={incident[2]} | "
            f"Risk={incident[3]}"
        )

    print("\n========== PIPELINE SUCCESS ==========\n")


if __name__ == "__main__":
    main()
