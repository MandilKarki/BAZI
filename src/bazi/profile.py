"""
BAZI profile management module.
"""
from pathlib import Path
import json
from typing import Dict, List, Optional
import random

class BaziProfileManager:
    def __init__(self, profiles_dir: str = 'profiles'):
        self.profiles_dir = Path(profiles_dir)
        self.profiles_dir.mkdir(exist_ok=True)
        
    def save_profile(self, user_data: Dict) -> str:
        """
        Save user profile to a JSON file.
        Returns: Filename of saved profile
        """
        # Create a filename from user's name
        safe_name = "".join(c for c in user_data["name"] if c.isalnum())
        filename = self.profiles_dir / f"{safe_name}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(user_data, f, indent=4)
            
        return str(filename)
    
    def load_profile(self, filename: str) -> Optional[Dict]:
        """Load a specific user profile."""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading profile {filename}: {str(e)}")
            return None
    
    def load_all_profiles(self) -> List[Dict]:
        """Load all user profiles."""
        profiles = []
        for profile_file in self.profiles_dir.glob('*.json'):
            if profile := self.load_profile(str(profile_file)):
                profiles.append(profile)
        return profiles
    
    def get_random_profile(self) -> Optional[Dict]:
        """Get a random profile from the profiles directory."""
        profile_files = list(self.profiles_dir.glob('baziprofiledata*.md'))
        if not profile_files:
            return None
        
        selected_file = random.choice(profile_files)
        try:
            with open(selected_file, 'r', encoding='utf-8') as f:
                return {"content": f.read(), "filename": str(selected_file)}
        except Exception as e:
            print(f"Error loading random profile: {str(e)}")
            return None
