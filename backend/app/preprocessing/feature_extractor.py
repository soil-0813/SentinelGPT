import logging
from typing import List, Dict, Optional
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def extract_hour_of_day(timestamp: str) -> Optional[int]:
    """
    Extract hour of day from timestamp string.
    
    Attempts to parse common timestamp formats and extract the hour.
    
    Args:
        timestamp: Timestamp string
        
    Returns:
        int: Hour of day (0-23) or None if parsing fails
    """
    if not timestamp:
        return None
    
    # Common timestamp formats to try
    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%dT%H:%M:%S.%fZ",
        "%d/%m/%Y %H:%M:%S",
        "%m/%d/%Y %H:%M:%S",
        "%Y/%m/%d %H:%M:%S",
    ]
    
    for fmt in formats:
        try:
            dt = datetime.strptime(timestamp, fmt)
            return dt.hour
        except ValueError:
            continue
    
    return None


def detect_failed_login(log_record: Dict) -> bool:
    """
    Detect if log represents a failed login attempt.
    
    Args:
        log_record: Log dictionary
        
    Returns:
        bool: True if failed login is detected
    """
    event_type = str(log_record.get("event_type", "")).lower()
    raw_log = log_record.get("raw_log", {})
    
    # Check event_type field
    if "failed_login" in event_type or "login_failed" in event_type or "failed" in event_type:
        return True
    
    # Check raw log for Windows event-related fields
    if log_record.get("log_source") == "windows":
        event_id = str(raw_log.get("event_id", "")).lower()
        event = str(raw_log.get("event", "")).lower()
        
        # Windows Event IDs for failed login: 4625 (failed login)
        if "4625" in event_id or "failed" in event or "failed_login" in event:
            return True
    
    return False


def detect_port_scan(log_record: Dict) -> bool:
    """
    Detect if log represents a port scan activity.
    
    Args:
        log_record: Log dictionary
        
    Returns:
        bool: True if port scan is detected
    """
    event_type = str(log_record.get("event_type", "")).lower()
    raw_log = log_record.get("raw_log", {})
    
    # Check event_type field
    if "port_scan" in event_type or "scan" in event_type:
        return True
    
    # Check raw log for port-related keywords
    action = str(raw_log.get("action", "")).lower()
    if "port" in action and "scan" in action:
        return True
    
    # Check alert_type for IDS
    alert_type = str(raw_log.get("alert_type", "")).lower()
    if "port_scan" in alert_type or "scan" in alert_type:
        return True
    
    return False


def detect_malware(log_record: Dict) -> bool:
    """
    Detect if log represents malware detection.
    
    Args:
        log_record: Log dictionary
        
    Returns:
        bool: True if malware is detected
    """
    event_type = str(log_record.get("event_type", "")).lower()
    raw_log = log_record.get("raw_log", {})
    
    # Check event_type field
    if "malware" in event_type or "malware_detected" in event_type:
        return True
    
    # Check alert_type for IDS
    alert_type = str(raw_log.get("alert_type", "")).lower()
    if "malware" in alert_type:
        return True
    
    # Check raw log message or description fields
    message = str(raw_log.get("message", "")).lower()
    description = str(raw_log.get("description", "")).lower()
    
    if "malware" in message or "malware" in description:
        return True
    
    return False


def detect_blocked_connection(log_record: Dict) -> bool:
    """
    Detect if log represents a blocked connection.
    
    Args:
        log_record: Log dictionary
        
    Returns:
        bool: True if blocked connection is detected
    """
    event_type = str(log_record.get("event_type", "")).lower()
    raw_log = log_record.get("raw_log", {})
    
    # Check action field (primarily for firewall logs)
    action = str(raw_log.get("action", "")).lower()
    if "block" in action or "blocked" in action or "denied" in action or "drop" in action:
        return True
    
    # Check event_type
    if "block" in event_type or "blocked" in event_type or "denied" in event_type:
        return True
    
    return False


def extract_features(logs: List[Dict]) -> List[Dict]:
    """
    Extract features from normalized logs.
    
    Generates feature sets for each log including:
    - Basic fields: source_ip, event_type, severity, timestamp, log_source
    - Temporal features: hour_of_day
    - Boolean indicators: is_failed_login, is_port_scan, is_malware, is_blocked_connection
    
    Args:
        logs: List of normalized log dictionaries from normalize_logs()
        
    Returns:
        List[Dict]: Logs enriched with feature extraction
    """
    if not isinstance(logs, list):
        logger.error(f"Expected list of logs, got {type(logs).__name__}")
        return []
    
    enriched_logs = []
    skipped_count = 0
    
    for idx, log_record in enumerate(logs):
        try:
            # Validate input is a dictionary
            if not isinstance(log_record, dict):
                logger.warning(f"Skipped record at index {idx}: not a dictionary")
                skipped_count += 1
                continue
            
            # Validate required fields exist
            required_fields = ["log_source", "timestamp", "source_ip", "event_type", "severity"]
            missing_fields = [field for field in required_fields if field not in log_record]
            
            if missing_fields:
                logger.warning(f"Skipped record at index {idx}: missing fields {missing_fields}")
                skipped_count += 1
                continue
            
            # Extract basic feature values
            source_ip = log_record.get("source_ip")
            event_type = log_record.get("event_type")
            severity = log_record.get("severity")
            timestamp = log_record.get("timestamp")
            log_source = log_record.get("log_source")
            
            # Extract temporal features
            hour_of_day = extract_hour_of_day(timestamp)
            
            # Extract boolean indicator features
            is_failed_login = detect_failed_login(log_record)
            is_port_scan = detect_port_scan(log_record)
            is_malware = detect_malware(log_record)
            is_blocked_connection = detect_blocked_connection(log_record)
            
            # Build features dictionary
            features = {
                "source_ip": source_ip,
                "event_type": event_type,
                "severity": severity,
                "timestamp": timestamp,
                "log_source": log_source,
                "hour_of_day": hour_of_day,
                "is_failed_login": is_failed_login,
                "is_port_scan": is_port_scan,
                "is_malware": is_malware,
                "is_blocked_connection": is_blocked_connection,
            }
            
            # Create enriched log record
            enriched_record = log_record.copy()
            enriched_record["log_features"] = features
            
            enriched_logs.append(enriched_record)
            
        except Exception as e:
            logger.error(f"Error processing record at index {idx}: {str(e)}")
            skipped_count += 1
            continue
    
    logger.info(f"Extracted features from {len(enriched_logs)} logs successfully, skipped {skipped_count} invalid records")
    
    return enriched_logs
