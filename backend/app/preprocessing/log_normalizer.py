import logging
from typing import List, Dict, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def normalize_logs(logs: List[Dict]) -> List[Dict]:
    """
    Normalize logs to a common schema.
    
    Converts logs from cleaner.py into a unified schema with standardized fields:
    - log_source: Source type (windows, firewall, ids)
    - timestamp: Log timestamp
    - source_ip: Source IP address
    - event_type: Normalized event type based on source
    - severity: Normalized severity level
    - raw_log: Original log record preserved as-is
    
    Args:
        logs: List of cleaned log dictionaries from clean_logs()
        
    Returns:
        List[Dict]: Normalized logs conforming to the common schema
    """
    if not isinstance(logs, list):
        logger.error(f"Expected list of logs, got {type(logs).__name__}")
        return []
    
    normalized_logs = []
    skipped_count = 0
    
    for idx, log_record in enumerate(logs):
        try:
            # Validate input is a dictionary
            if not isinstance(log_record, dict):
                logger.warning(f"Skipped record at index {idx}: not a dictionary")
                skipped_count += 1
                continue
            
            # Extract required fields
            log_source = log_record.get("log_source")
            timestamp = log_record.get("timestamp")
            source_ip = log_record.get("source_ip")
            
            # Validate log_source exists
            if not log_source:
                logger.warning(f"Skipped record at index {idx}: missing or empty log_source")
                skipped_count += 1
                continue
            
            # Validate timestamp exists
            if not timestamp:
                logger.warning(f"Skipped record at index {idx} ({log_source}): missing or empty timestamp")
                skipped_count += 1
                continue
            
            # Determine event_type and severity based on log_source
            event_type = None
            severity = None
            
            if log_source == "windows":
                event_type = log_record.get("event")
                severity = "low"
                
                if not event_type:
                    logger.warning(f"Skipped record at index {idx} (windows): missing event field")
                    skipped_count += 1
                    continue
                
                # Windows logs may not have source_ip, use empty string
                if not source_ip:
                    source_ip = ""
            
            elif log_source == "firewall":
                event_type = log_record.get("action")
                severity = "medium"
                
                if not event_type:
                    logger.warning(f"Skipped record at index {idx} (firewall): missing action field")
                    skipped_count += 1
                    continue
                
                if not source_ip:
                    logger.warning(f"Skipped record at index {idx} (firewall): missing source_ip")
                    skipped_count += 1
                    continue
            
            elif log_source == "ids":
                event_type = log_record.get("alert_type")
                severity = log_record.get("severity")
                
                if not event_type:
                    logger.warning(f"Skipped record at index {idx} (ids): missing alert_type field")
                    skipped_count += 1
                    continue
                
                if not severity:
                    logger.warning(f"Skipped record at index {idx} (ids): missing severity field")
                    skipped_count += 1
                    continue
                
                if not source_ip:
                    logger.warning(f"Skipped record at index {idx} (ids): missing source_ip")
                    skipped_count += 1
                    continue
            
            else:
                logger.warning(f"Skipped record at index {idx}: unknown log_source type '{log_source}'")
                skipped_count += 1
                continue
            
            # Create normalized log record
            normalized_record = {
                "log_source": log_source,
                "timestamp": timestamp,
                "source_ip": source_ip,
                "event_type": event_type,
                "severity": severity,
                "raw_log": log_record.copy()
            }
            
            normalized_logs.append(normalized_record)
            
        except Exception as e:
            logger.error(f"Error processing record at index {idx}: {str(e)}")
            skipped_count += 1
            continue
    
    logger.info(f"Normalized {len(normalized_logs)} logs successfully, skipped {skipped_count} invalid records")
    
    return normalized_logs
