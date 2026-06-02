from pathlib import Path
import json
import logging
from typing import List, Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def read_windows_logs(file_path: str = "windows_logs.json") -> List[Dict[str, Any]]:
    """
    Read Windows logs from a JSON file and return as a list of dictionaries.

    This function reads a JSON file containing Windows log entries, validates
    the JSON format, and returns the data as a list of dictionaries.

    Args:
        file_path: Path to the JSON file containing Windows logs.
                  Defaults to "windows_logs.json" in the current directory.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries where each dictionary
                             represents a Windows log entry.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        json.JSONDecodeError: If the file contains invalid JSON.
        TypeError: If the JSON content is not a list of dictionaries.

    Examples:
        >>> logs = read_windows_logs()
        >>> len(logs)
        10
        >>> logs[0]['event_id']
        1001
    """
    path = Path(file_path)

    if not path.exists():
        logger.error(f"File not found: {path.absolute()}")
        raise FileNotFoundError(f"Windows logs file not found: {path.absolute()}")

    if not path.is_file():
        logger.error(f"Path is not a file: {path.absolute()}")
        raise FileNotFoundError(f"Path is not a file: {path.absolute()}")

    logger.info(f"Reading Windows logs from: {path.absolute()}")

    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in file {path.absolute()}: {str(e)}")
        raise json.JSONDecodeError(
            f"Invalid JSON in file: {path.absolute()}",
            e.doc,
            e.pos
        )

    if not isinstance(data, list):
        logger.error(f"JSON content is not a list: {type(data)}")
        raise TypeError(f"Expected JSON content to be a list, got {type(data).__name__}")

    for i, item in enumerate(data):
        if not isinstance(item, dict):
            logger.error(f"Item at index {i} is not a dictionary: {type(item)}")
            raise TypeError(
                f"Expected all items to be dictionaries, "
                f"item at index {i} is {type(item).__name__}"
            )

    logger.info(f"Successfully read {len(data)} log entries from {path.name}")
    return data


if __name__ == "__main__":
    try:
        logs = read_windows_logs()
        print(f"Successfully loaded {len(logs)} log entries")
        if logs:
            print(f"First entry: {logs[0]}")
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except json.JSONDecodeError as e:
        print(f"JSON Error: {e}")
    except TypeError as e:
        print(f"Type Error: {e}")