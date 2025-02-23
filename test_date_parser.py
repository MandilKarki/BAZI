"""
Test script for BAZI date parsing and reading functionality.
"""
from datetime import datetime
import pandas as pd
import re
from typing import Optional, Tuple, Dict

class BaziDateParser:
    def __init__(self, bazi_data_file: str):
        """Initialize with path to BAZI data CSV file."""
        self.bazi_data_file = bazi_data_file
        self.bazi_df = None
        self._load_data()
        
    def _load_data(self):
        """Load BAZI data from CSV file."""
        try:
            self.bazi_df = pd.read_csv(self.bazi_data_file)
            # Convert date strings to datetime
            self.bazi_df['Date'] = pd.to_datetime(self.bazi_df['Date'], format='%a %m/%d/%Y')
            print(f"Loaded {len(self.bazi_df)} BAZI readings")
        except Exception as e:
            print(f"Error loading BAZI data: {str(e)}")
            
    def parse_date(self, text: str) -> Optional[datetime]:
        """Parse date from text using multiple methods."""
        # Try parsing relative dates
        relative_date = self._parse_relative_date(text)
        if relative_date:
            return relative_date
            
        # Try parsing explicit dates
        explicit_date = self._parse_explicit_date(text)
        if explicit_date:
            return explicit_date
            
        return None
        
    def _parse_relative_date(self, text: str) -> Optional[datetime]:
        """Parse relative date references."""
        today = datetime.now()
        text = text.lower()
        
        if 'today' in text:
            return today
        elif 'tomorrow' in text:
            return today.replace(day=today.day + 1)
        elif 'yesterday' in text:
            return today.replace(day=today.day - 1)
            
        return None
        
    def _parse_explicit_date(self, text: str) -> Optional[datetime]:
        """Parse explicit date formats."""
        # Common date patterns
        patterns = [
            r'(\d{1,2}/\d{1,2}/\d{4})',  # MM/DD/YYYY
            r'(\d{4}-\d{2}-\d{2})',      # YYYY-MM-DD
            r'(Feb(?:ruary)?\s+\d{1,2}(?:st|nd|rd|th)?,?\s+\d{4})'  # February 1st, 2024
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                try:
                    date_str = match.group(1)
                    return pd.to_datetime(date_str)
                except:
                    continue
        return None
    
    def get_bazi_reading(self, date: datetime) -> Optional[Dict]:
        """Get BAZI reading for the specified date."""
        if self.bazi_df is None:
            return None
            
        try:
            # Find the reading for the exact date
            daily_data = self.bazi_df[self.bazi_df['Date'].dt.date == date.date()]
            
            if daily_data.empty:
                print(f"No BAZI reading found for {date.date()}")
                return None
                
            reading = daily_data.iloc[0].to_dict()
            print(f"Found BAZI reading for {date.date()}:")
            print(f"Day Pillar: {reading['Day Pillar']} ({reading['Day Pillar English']})")
            print(f"Day Officer: {reading['Day Officer']}")
            return reading
            
        except Exception as e:
            print(f"Error getting BAZI reading: {str(e)}")
            return None

def test_date_parser():
    """Run tests for date parsing and BAZI reading."""
    parser = BaziDateParser('Feb 2025 Bazi.csv')
    
    # Test cases
    test_inputs = [
        "What's my reading for February 1st, 2025?",
        "Tell me about 2/2/2025",
        "Show me today's reading",
        "What about tomorrow?",
        "Analysis for 2025-02-15",
    ]
    
    print("\nRunning test cases...")
    print("-" * 50)
    
    for input_text in test_inputs:
        print(f"\nTesting input: '{input_text}'")
        date = parser.parse_date(input_text)
        
        if date:
            print(f"Parsed date: {date.date()}")
            reading = parser.get_bazi_reading(date)
            if reading:
                print("✓ Successfully retrieved BAZI reading")
        else:
            print("✗ Could not parse date from input")
        print("-" * 30)

if __name__ == "__main__":
    test_date_parser()
