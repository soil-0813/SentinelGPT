"""
Log loader module for aggregating logs from multiple sources.

This module provides functionality to load and consolidate log entries from
multiple JSON log files. It includes error handling and detailed logging
for monitoring the log loading process.
"""

from typing import List, Dict, Any
import logging
from pathlib import Path

from .windows_logs import read_windows_logs

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_all_logs(
    log_files: List[str] = None
) -> List[Dict[str, Any]]:
    """
    Load all available logs from multiple log files and return as a single list.

    This function aggregates logs from multiple Windows log JSON files into a
    unified list. By default, it loads from 'windows_logs.json'. Additional
    log files can be specified via the log_files parameter.

    Args:
        log_files: List of paths to JSON log files. If None, defaults to
                  ['datasets/logs/windows_logs.json']. Each file should contain
                  a JSON array of log entry dictionaries.

    Returns:
        List[Dict[str, Any]]: A consolidated list of all log entries from
                             all successfully loaded files. Duplicate entries
                             are preserved.

    Raises:
        Exception: Catches and logs all exceptions during file loading.
                   Individual file failures do not stop the process;
                   only successfully loaded logs are returned.

    Examples:
        >>> all_logs = load_all_logs()
        >>> len(all_logs)
        50
        >>> all_logs = load_all_logs(['datasets/logs/windows_logs.json', 'datasets/logs/system_logs.json'])
        >>> len(all_logs)
        120
    """
    if log_files is None:
        log_files = ["datasets/logs/windows_logs.json"]

    logger.info(f"Starting to load logs from {len(log_files)} file(s)")

    all_logs: List[Dict[str, Any]] = []
    successful_loads = 0
    failed_loads = 0
    total_entries_loaded = 0

    for file_path in log_files:
        try:
            logger.info(f"Loading logs from: {file_path}")
            logs = read_windows_logs(file_path)
            all_logs.extend(logs)
            entries_count = len(logs)
            total_entries_loaded += entries_count
            successful_loads += 1
            logger.info(
                f"Successfully loaded {entries_count} entries from {file_path}"
            )

        except FileNotFoundError as e:
            logger.warning(f"File not found, skipping: {file_path} - {str(e)}")
            failed_loads += 1

        except Exception as e:
            logger.error(
                f"Error loading {file_path}: {type(e).__name__} - {str(e)}"
            )
            failed_loads += 1

    logger.info(
        f"Log loading complete: {successful_loads} succeeded, "
        f"{failed_loads} failed"
    )
    logger.info(f"Total log entries loaded: {len(all_logs)}")

    return all_logs


if __name__ == "__main__":
    try:
        # Load from default file
        logs = load_all_logs()
        print(f"✓ Total logs loaded: {len(logs)}")

        # Example: Load from multiple files
        # multi_logs = load_all_logs([
        #     "datasets/logs/windows_logs.json",
        #     "datasets/logs/system_logs.json",
        #     "datasets/logs/application_logs.json"
        # ])
        # print(f"✓ Total logs from multiple files: {len(multi_logs)}")

    except Exception as e:
        print(f"✗ Unexpected error: {type(e).__name__} - {str(e)}")