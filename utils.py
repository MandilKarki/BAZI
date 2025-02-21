from datetime import datetime
from typing import Dict, Any
import pytz

def validate_birth_datetime(date_str: str, time_str: str, timezone_str: str) -> bool:
    """Validate birth date, time and timezone input."""
    try:
        # Validate date format
        datetime.strptime(date_str, "%Y-%m-%d")
        
        # Validate time format
        datetime.strptime(time_str, "%H:%M")
        
        # Validate timezone format (simple UTC offset validation)
        if not (timezone_str.startswith("UTC+") or timezone_str.startswith("UTC-")):
            return False
        int(timezone_str[4:])  # Should be a number after UTC+/-
        
        return True
    except ValueError:
        return False

def format_bazi_data(bazi_data: Dict[str, Any]) -> str:
    """Format Bazi data into a readable string."""
    return f"""
Year Pillar: {bazi_data['year_pillar']}
Month Pillar: {bazi_data['month_pillar']}
Day Pillar: {bazi_data['day_pillar']}
Hour Pillar: {bazi_data['hour_pillar']}
Day Officer: {bazi_data['day_officer']}
"""
