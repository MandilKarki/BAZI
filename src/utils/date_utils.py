"""
Date handling utilities for BAZI Profile System.
"""
from datetime import datetime
import pytz
from typing import Optional, Tuple

def parse_date(date_str: str) -> Optional[datetime]:
    """Try to parse date string in multiple formats."""
    date_formats = [
        "%Y-%m-%d",  # 2024-02-20
        "%d-%m-%Y",  # 20-02-2024
        "%m-%d-%Y",  # 02-20-2024
        "%d/%m/%Y",  # 20/02/2024
        "%m/%d/%Y",  # 02/20/2024
        "%Y/%m/%d",  # 2024/02/20
        "%d.%m.%Y",  # 20.02.2024
        "%m.%d.%Y",  # 02.20.2024
        "%Y.%m.%d",  # 2024.02.20
    ]
    
    for fmt in date_formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return None

def validate_birth_datetime(date_str: str, time_str: str, timezone_str: str) -> Tuple[bool, str]:
    """
    Validate birth date, time and timezone input.
    Returns: (is_valid: bool, error_message: str)
    """
    try:
        # Validate date
        if not parse_date(date_str):
            return False, "Invalid date format"
        
        # Validate time
        try:
            datetime.strptime(time_str, "%H:%M")
        except ValueError:
            return False, "Invalid time format. Use HH:MM (24-hour)"
        
        # Validate timezone
        if timezone_str not in pytz.all_timezones:
            return False, "Invalid timezone"
        
        return True, ""
    except Exception as e:
        return False, f"Validation error: {str(e)}"
