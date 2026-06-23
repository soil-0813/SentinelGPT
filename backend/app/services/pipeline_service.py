from app.data_sources.log_loader import load_all_logs

from app.preprocessing.parser import parse_logs
from app.preprocessing.cleaner import clean_logs
from app.preprocessing.log_normalizer import normalize_logs
from app.preprocessing.feature_extractor import extract_features

from app.detection.detector import (
    detect_attacks,
    build_incidents
)


def run_detection_pipeline():
    """
    Executes the complete SentinelGPT pipeline.

    Returns:
        {
            "alerts": [...],
            "incidents": [...],
            "total_logs": int,
            "processed_logs": int
        }
    """

    # ---------------------------------
    # Load Logs
    # ---------------------------------

    raw_logs = load_all_logs()

    # ---------------------------------
    # Parse
    # ---------------------------------

    parsed_logs = parse_logs(raw_logs)

    # ---------------------------------
    # Clean
    # ---------------------------------

    cleaned_logs = clean_logs(parsed_logs)

    # ---------------------------------
    # Normalize
    # ---------------------------------

    normalized_logs = normalize_logs(cleaned_logs)

    # ---------------------------------
    # Feature Extraction
    # ---------------------------------

    featured_logs = extract_features(normalized_logs)

    # ---------------------------------
    # Detection Engine
    # ---------------------------------

    alerts = detect_attacks(featured_logs)

    # ---------------------------------
    # Incident Builder
    # ---------------------------------

    incidents = build_incidents(alerts)

    return {
        "alerts": alerts,
        "incidents": incidents,
        "total_logs": len(raw_logs),
        "processed_logs": len(featured_logs)
    }


def get_alerts():
    """
    Returns only alerts.
    """

    result = run_detection_pipeline()

    return result["alerts"]


def get_incidents():
    """
    Returns only incidents.
    """

    result = run_detection_pipeline()

    return result["incidents"]