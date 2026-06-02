"""
Log loader module for aggregating logs from multiple sources.

This module loads and combines:
- Windows Logs
- Firewall Logs
- IDS Alerts

into a single unified dataset.
"""

from typing import List, Dict, Any
import logging

from .windows_logs import read_windows_logs
from .firewall_logs import load_firewall_logs
from .ids_alerts import load_ids_alerts

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def load_all_logs() -> List[Dict[str, Any]]:
    """
    Load all log sources and combine them into a single list.

    Returns:
        List[Dict[str, Any]]:
            Combined logs from Windows, Firewall and IDS sources.
    """

    logger.info("Starting SentinelGPT log collection")

    all_logs: List[Dict[str, Any]] = []

    successful_loads = 0
    failed_loads = 0

    log_sources = [
        (
            "Windows Logs",
            "datasets/logs/windows_logs.json",
            read_windows_logs
        ),
        (
            "Firewall Logs",
            "datasets/logs/firewall_logs.json",
            load_firewall_logs
        ),
        (
            "IDS Alerts",
            "datasets/logs/ids_alerts.json",
            load_ids_alerts
        )
    ]

    for source_name, file_path, loader_function in log_sources:

        try:
            logger.info(f"Loading {source_name}")

            logs = loader_function(file_path)

            all_logs.extend(logs)

            successful_loads += 1

            logger.info(
                f"{source_name}: {len(logs)} records loaded successfully"
            )

        except Exception as e:

            failed_loads += 1

            logger.error(
                f"{source_name} failed: "
                f"{type(e).__name__} - {str(e)}"
            )

    logger.info(
        f"Log loading complete "
        f"({successful_loads} succeeded, "
        f"{failed_loads} failed)"
    )

    logger.info(
        f"Total records collected: {len(all_logs)}"
    )

    return all_logs


if __name__ == "__main__":

    logs = load_all_logs()

    print("\n========== SENTINELGPT TEST ==========")
    print(f"Total records loaded: {len(logs)}")

    print("\nFirst 5 records:\n")

    for log in logs[:5]:
        print(log)