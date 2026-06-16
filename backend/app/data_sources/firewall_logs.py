"""
Firewall logs data loader module.

This module provides functionality to load and parse firewall log events
from a JSON dataset file. It includes comprehensive error handling for
file I/O and JSON parsing operations, with detailed logging for debugging
and monitoring.
"""

import json
import logging
from pathlib import Path
from typing import Dict, List

# Configure module logger
logger = logging.getLogger(__name__)


def load_firewall_logs(file_path: str | Path = "datasets/firewall_logs.json") -> List[Dict]:
    """
    Load firewall log events from a JSON file.

    This function reads a JSON file containing firewall events and returns
    them as a list of dictionaries. It validates the JSON structure and
    ensures the data contains required fields.

    Args:
        file_path: Path to the firewall_logs.json file. Defaults to
            "datasets/firewall_logs.json" relative to the current working directory.
            Can be a string or pathlib.Path object.

    Returns:
        A list of dictionaries, each representing a firewall event with
        fields: event_id, timestamp, source_ip, destination_ip, port,
        protocol, and action.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        json.JSONDecodeError: If the file contains invalid JSON.
        ValueError: If the JSON structure is invalid or required fields are missing.

    Example:
        >>> logs = load_firewall_logs()
        >>> print(f"Loaded {len(logs)} firewall events")
        >>> print(logs[0].keys())
    """
    # Convert to Path object for consistent path handling
    file_path = Path(file_path)

    logger.info(f"Loading firewall logs from: {file_path.absolute()}")

    # Validate file exists
    if not file_path.exists():
        error_msg = f"Firewall logs file not found: {file_path}"
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
        error_msg = f"Invalid JSON in firewall logs file: {e}"
        logger.error(error_msg)
        raise json.JSONDecodeError(error_msg, e.doc, e.pos) from e
    except IOError as e:
        error_msg = f"Error reading firewall logs file: {e}"
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
        logger.warning("Firewall logs file is empty")
        return []

    # Validate each event and required fields
    required_fields = {
        "event_id",
        "timestamp",
        "source_ip",
        "destination_ip",
        "port",
        "protocol",
        "action",
    }

    validated_logs: List[Dict] = []

    for idx, event in enumerate(data):
        if not isinstance(event, dict):
            error_msg = (
                f"Invalid structure at index {idx}: expected dictionary, "
                f"got {type(event).__name__}"
            )
            logger.error(error_msg)
            raise ValueError(error_msg)

        # Check for missing required fields
        missing_fields = required_fields - set(event.keys())
        if missing_fields:
            error_msg = (
                f"Missing required fields at index {idx}: {missing_fields}. "
                f"Event: {event}"
            )
            logger.error(error_msg)
            raise ValueError(error_msg)

        validated_logs.append(event)

    logger.info(f"Successfully loaded {len(validated_logs)} firewall events")
    return validated_logs


if __name__ == "__main__":
    # Configure logging for standalone execution
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    try:
        firewall_events = load_firewall_logs()
        print(f"✓ Loaded {len(firewall_events)} firewall events")
        if firewall_events:
            print(f"✓ First event: {firewall_events[0]}")
    except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
        print(f"✗ Error: {e}")
