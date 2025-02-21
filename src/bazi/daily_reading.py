"""
Daily BAZI readings and analysis module.
"""
import pandas as pd
from datetime import datetime
from typing import Dict, Optional, Any

class DailyBaziReader:
    def __init__(self, data_file: str):
        """Initialize with path to BAZI data CSV file."""
        self.data_file = data_file
        self.daily_bazi_df = None
        self.load_data()
    
    def load_data(self) -> None:
        """Load daily Bazi data from CSV file."""
        try:
            self.daily_bazi_df = pd.read_csv(self.data_file)
            # Convert date column to datetime
            self.daily_bazi_df['Date'] = pd.to_datetime(self.daily_bazi_df['Date'])
        except Exception as e:
            print(f"Error loading daily BAZI data: {str(e)}")
            self.daily_bazi_df = None
    
    def get_daily_reading(self, date: str) -> Optional[Dict[str, Any]]:
        """
        Get BAZI reading for a specific date.
        Args:
            date: Date string in YYYY-MM-DD format
        Returns:
            Dictionary containing BAZI reading data
        """
        if self.daily_bazi_df is None:
            return None
            
        try:
            target_date = pd.to_datetime(date)
            daily_data = self.daily_bazi_df[self.daily_bazi_df['Date'] == target_date]
            
            if daily_data.empty:
                return None
                
            return daily_data.iloc[0].to_dict()
        except Exception as e:
            print(f"Error getting daily reading: {str(e)}")
            return None
    
    def format_reading(self, bazi_data: Dict[str, Any]) -> str:
        """Format BAZI data into a readable string."""
        if not bazi_data:
            return "No BAZI data available"
            
        return f"""
        Date: {bazi_data['Date']}
        
        Pillars:
        - Year: {bazi_data['Year Pillar Chinese']} ({bazi_data['Year Pillar English']})
        - Month: {bazi_data['Month Pillar Chinese']} ({bazi_data['Month Pillar English']})
        - Day: {bazi_data['Day Pillar Chinese']} ({bazi_data['Day Pillar English']})
        
        Day Officer: {bazi_data['Day Officer']}
        """
