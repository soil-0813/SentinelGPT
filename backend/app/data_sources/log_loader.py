"""
SentinelGPT Log Loader

Loads logs from:
1. Windows Logs
2. Firewall Logs
3. IDS Alerts

Combines everything into a single list for preprocessing.
"""

import logging
from typing import List, Dict, Any

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
    Load all security logs from all available data sources.

    Returns:
        Combined list containing:
        - Windows events
        - Firewall events
        - IDS alerts
    """

    all_logs = []

    successful_loads = 0
    failed_loads = 0

    logger.info("Starting SentinelGPT log collection")

    # --------------------------
    # WINDOWS LOGS
    # --------------------------
    try:
        logger.info("Loading Windows Logs")

        windows_logs = read_windows_logs(
            "datasets/logs/windows_logs.json"
        )

        all_logs.extend(windows_logs)

        logger.info(
            f"Windows Logs: {len(windows_logs)} records loaded successfully"
        )

        successful_loads += 1

    except Exception as e:
        logger.error(f"Windows Logs Error: {e}")
        failed_loads += 1

    # --------------------------
    # FIREWALL LOGS
    # --------------------------
    try:
        logger.info("Loading Firewall Logs")

        firewall_logs = load_firewall_logs(
            "datasets/logs/firewall_logs.json"
        )

        all_logs.extend(firewall_logs)

        logger.info(
            f"Firewall Logs: {len(firewall_logs)} records loaded successfully"
        )

        successful_loads += 1

    except Exception as e:
        logger.error(f"Firewall Logs Error: {e}")
        failed_loads += 1

    # --------------------------
    # IDS ALERTS
    # --------------------------
    try:
        logger.info("Loading IDS Alerts")

        ids_alerts = load_ids_alerts(
            "datasets/logs/ids_alerts.json"
        )

        all_logs.extend(ids_alerts)

        logger.info(
            f"IDS Alerts: {len(ids_alerts)} records loaded successfully"
        )

        successful_loads += 1

    except Exception as e:
        logger.error(f"IDS Alerts Error: {e}")
        failed_loads += 1

    logger.info(
        f"Log loading complete ({successful_loads} succeeded, {failed_loads} failed)"
    )

    logger.info(
        f"Total records collected: {len(all_logs)}"
    )

    return all_logs


if __name__ == "__main__":

    logs = load_all_logs()

    print("\n========== TEST RESULTS ==========")
    print(f"Total records loaded: {len(logs)}")

    windows_count = sum(
        1 for log in logs if "username" in log
    )

    firewall_count = sum(
        1 for log in logs if "destination_ip" in log
    )

    ids_count = sum(
        1 for log in logs if "alert_type" in log
    )

    print("\nVerification:")
    print(f"Windows Logs : {windows_count}")
    print(f"Firewall Logs: {firewall_count}")
    print(f"IDS Alerts   : {ids_count}")