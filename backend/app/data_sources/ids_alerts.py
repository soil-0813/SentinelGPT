"""
IDS alerts data loader module.

This module provides functionality to load and parse IDS (Intrusion Detection System)
alert events from a JSON dataset file. It includes comprehensive error handling for
file I/O and JSON parsing operations, with detailed logging for debugging and monitoring.
"""

import json
import logging
from pathlib import Path
from typing import Dict, List

# Configure module logger
logger = logging.getLogger(__name__)


def load_ids_alerts(file_path: str | Path = "datasets/ids_alerts.json") -> List[Dict]:
    """
    Load IDS alert events from a JSON file.

    This function reads a JSON file containing IDS alert events and returns
    them as a list of dictionaries. It validates the JSON structure and
    ensures the data contains required fields.

    Args:
        file_path: Path to the ids_alerts.json file. Defaults to
            "datasets/ids_alerts.json" relative to the current working directory.
            Can be a string or pathlib.Path object.

    Returns:
        A list of dictionaries, each representing an IDS alert with
        fields: alert_id, timestamp, source_ip, alert_type, severity,
        and description.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        json.JSONDecodeError: If the file contains invalid JSON.
        ValueError: If the JSON structure is invalid or required fields are missing.

    Example:
        >>> alerts = load_ids_alerts()
        >>> print(f"Loaded {len(alerts)} IDS alerts")
        >>> print(alerts[0].keys())
    """
    # Convert to Path object for consistent path handling
    file_path = Path(file_path)

    logger.info(f"Loading IDS alerts from: {file_path.absolute()}")

    # Validate file exists
    if not file_path.exists():
        error_msg = f"IDS alerts file not found: {file_path}"
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)

    if not file_path.is_file():
        error_msg = f"Path is not a file: {file_path}"
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)

    # Read and parse JSON file
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        logger.debug(f"Successfully parsed JSON from {file_path}")
    except json.JSONDecodeError as e:
        error_msg = f"Invalid JSON in IDS alerts file: {e}"
        logger.error(error_msg)
        raise json.JSONDecodeError(error_msg, e.doc, e.pos) from e
    except IOError as e:
        error_msg = f"Error reading IDS alerts file: {e}"
        logger.error(error_msg)
        raise FileNotFoundError(error_msg) from e

    # Validate data structure
    if not isinstance(data, list):
        error_msg = (
            f"Invalid structure: expected JSON array at root level, "
            f"got {type(data).__name__}"
        )
        logger.error(error_msg)
        raise ValueError(error_msg)

    if not data:
        logger.warning("IDS alerts file is empty")
        return []

    # Validate each alert and required fields
    required_fields = {
        "alert_id",
        "timestamp",
        "source_ip",
        "alert_type",
        "severity",
        "description",
    }

    validated_alerts: List[Dict] = []

    for idx, alert in enumerate(data):
        if not isinstance(alert, dict):
            error_msg = (
                f"Invalid structure at index {idx}: expected dictionary, "
                f"got {type(alert).__name__}"
            )
            logger.error(error_msg)
            raise ValueError(error_msg)

        # Check for missing required fields
        missing_fields = required_fields - set(alert.keys())
        if missing_fields:
            error_msg = (
                f"Missing required fields at index {idx}: {missing_fields}. "
                f"Alert: {alert}"
            )
            logger.error(error_msg)
            raise ValueError(error_msg)

        validated_alerts.append(alert)

    logger.info(f"Successfully loaded {len(validated_alerts)} IDS alerts")
    return validated_alerts


if __name__ == "__main__":
    # Configure logging for standalone execution
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    try:
        alerts = load_ids_alerts()
        print(f"✓ Loaded {len(alerts)} IDS alerts")
        if alerts:
            print(f"✓ First alert: {alerts[0]}")
    except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
        print(f"✗ Error: {e}")
