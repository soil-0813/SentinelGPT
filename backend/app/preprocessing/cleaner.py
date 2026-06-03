import logging
from typing import List, Dict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def clean_logs(logs: List[Dict]) -> List[Dict]:
    """
    Clean and validate logs from parser.py.
    
    Removes invalid records while preserving valid logs. Performs the following checks:
    - Removes non-dictionary records
    - Removes empty dictionaries
    - Removes records missing timestamp
    - Removes records missing source_ip (except Windows logs with username and event)
    - Removes records missing log_source field
    
    Args:
        logs: List of log dictionaries from parse_logs()
        
    Returns:
        List[Dict]: Cleaned and validated logs
    """
    if not isinstance(logs, list):
        logger.error(f"Expected list of logs, got {type(logs).__name__}")
        return []
    
    cleaned_logs = []
    removed_count = 0
    
    for idx, log_record in enumerate(logs):
        try:
            # Check 1: Remove non-dictionary records
            if not isinstance(log_record, dict):
                logger.debug(f"Removed record at index {idx}: not a dictionary (type: {type(log_record).__name__})")
                removed_count += 1
                continue
            
            # Check 2: Remove empty dictionaries
            if not log_record:
                logger.debug(f"Removed record at index {idx}: empty dictionary")
                removed_count += 1
                continue
            
            # Check 5: Remove records missing log_source field
            if "log_source" not in log_record:
                logger.debug(f"Removed record at index {idx}: missing log_source field")
                removed_count += 1
                continue
            
            log_source = log_record.get("log_source")
            
            # Check 3: Remove records missing timestamp
            if "timestamp" not in log_record:
                logger.debug(f"Removed record at index {idx} ({log_source}): missing timestamp field")
                removed_count += 1
                continue
            
            # Check 4: Remove records missing source_ip (with exception for Windows logs)
            if log_source == "windows":
                # Windows logs may not contain source_ip - keep if username and event exist
                if "username" not in log_record or "event" not in log_record:
                    logger.debug(f"Removed record at index {idx} (windows): missing username or event field")
                    removed_count += 1
                    continue
            else:
                # Non-Windows logs must have source_ip
                if "source_ip" not in log_record:
                    logger.debug(f"Removed record at index {idx} ({log_source}): missing source_ip field")
                    removed_count += 1
                    continue
            
            # Record is valid - add to cleaned logs
            cleaned_logs.append(log_record)
            
        except Exception as e:
            logger.error(f"Error processing record at index {idx}: {str(e)}")
            removed_count += 1
            continue
    
    logger.info(f"Cleaned {len(cleaned_logs)} valid logs, removed {removed_count} invalid records")
    
    return cleaned_logs
