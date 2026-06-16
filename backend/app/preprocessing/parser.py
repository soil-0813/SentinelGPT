import logging
from typing import List, Dict, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def detect_source_type(log_record: Dict) -> Optional[str]:
    """
    Detect the source type of a log record based on its keys.
    
    Args:
        log_record: A dictionary representing a single log entry
        
    Returns:
        str: The detected source type ("windows", "firewall", "ids") or None if not recognized
    """
    if not isinstance(log_record, dict):
        return None
    
    keys = set(log_record.keys())
    
    # Check for Windows logs
    if "username" in keys and "event" in keys:
        return "windows"
    
    # Check for Firewall logs
    if "destination_ip" in keys and "action" in keys:
        return "firewall"
    
    # Check for IDS logs
    if "alert_type" in keys and "severity" in keys:
        return "ids"
    
    return None


def parse_logs(logs: List[Dict]) -> List[Dict]:
    """
    Parse and tag logs with their source type.
    
    Accepts a list of log dictionaries from load_all_logs(), detects the source type
    based on identifying keys, and adds a "log_source" field to each record. Invalid
    records are skipped safely with logging.
    
    Args:
        logs: List of log dictionaries from load_all_logs()
        
    Returns:
        List[Dict]: Parsed logs with "log_source" field added and all original fields preserved
    """
    if not isinstance(logs, list):
        logger.error(f"Expected list of logs, got {type(logs).__name__}")
        return []
    
    parsed_logs = []
    skipped_count = 0
    
    for idx, log_record in enumerate(logs):
        try:
            # Validate that the record is a dictionary
            if not isinstance(log_record, dict):
                logger.warning(f"Skipped record at index {idx}: expected dict, got {type(log_record).__name__}")
                skipped_count += 1
                continue
            
            # Detect the source type
            source_type = detect_source_type(log_record)
            
            if source_type is None:
                logger.warning(f"Skipped record at index {idx}: unable to determine log source type")
                skipped_count += 1
                continue
            
            # Create a new record with all original fields plus log_source
            parsed_record = log_record.copy()
            parsed_record["log_source"] = source_type
            
            parsed_logs.append(parsed_record)
            
        except Exception as e:
            logger.error(f"Error processing record at index {idx}: {str(e)}")
            skipped_count += 1
            continue
    
    logger.info(f"Parsed {len(parsed_logs)} logs successfully, skipped {skipped_count} invalid records")
    
    return parsed_logs
