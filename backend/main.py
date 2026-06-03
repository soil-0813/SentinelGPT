from app.data_sources.log_loader import load_all_logs

from app.preprocessing.parser import parse_logs
from app.preprocessing.cleaner import clean_logs
from app.preprocessing.log_normalizer import normalize_logs
from app.preprocessing.feature_extractor import extract_features


def main():

    print("\n========== SENTINELGPT PIPELINE TEST ==========\n")

    # Load logs
    raw_logs = load_all_logs()
    print(f"Raw logs loaded: {len(raw_logs)}")

    # Parse logs
    parsed_logs = parse_logs(raw_logs)
    print(f"Parsed logs: {len(parsed_logs)}")

    # Clean logs
    cleaned_logs = clean_logs(parsed_logs)
    print(f"Cleaned logs: {len(cleaned_logs)}")

    # Normalize logs
    normalized_logs = normalize_logs(cleaned_logs)
    print(f"Normalized logs: {len(normalized_logs)}")

    # Extract features
    feature_logs = extract_features(normalized_logs)
    print(f"Feature enriched logs: {len(feature_logs)}")

    print("\n========== SAMPLE OUTPUT ==========\n")

    if feature_logs:
        print(feature_logs[0])

    print("\n========== PIPELINE SUCCESS ==========\n")


if __name__ == "__main__":
    main()
