def generate_attack_summary(incident_data: dict) -> str:
    """
    Generate a concise text summary of an attack based on the incident data.
    """
    attack_type = incident_data.get('attack_type', 'Unknown Attack')
    timeline = incident_data.get('timeline', [])
    
    summary = f"Detected {attack_type} activity. "
    if timeline:
        summary += f"The attack timeline contains {len(timeline)} key events. "
        
    reasoning = incident_data.get('reasoning', [])
    if reasoning:
        summary += "Based on correlation engine analysis, the following patterns were observed: "
        summary += " ".join(reasoning)
        
    return summary
