import json
import logging
from pathlib import Path
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class UserProfile:
    def __init__(self, profile_path: str):
        """
        Initialize the User Profile manager.
        
        Args:
            profile_path: Path to the user_profile.json file.
        """
        self.profile_path = Path(profile_path)
        self.profile_data: Dict[str, Any] = self._load_profile()

    def _load_profile(self) -> Dict[str, Any]:
        """Load profile from disk or create default."""
        if self.profile_path.exists():
            try:
                with open(self.profile_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Failed to load profile: {e}")
                return self._default_profile()
        else:
            return self._default_profile()

    def _default_profile(self) -> Dict[str, Any]:
        """Return a default empty profile."""
        return {
            "name": "User",
            "interests": [],
            "preferences": {},
            "facts": {}
        }

    def save_profile(self):
        """Save current profile to disk."""
        try:
            with open(self.profile_path, 'w') as f:
                json.dump(self.profile_data, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save profile: {e}")

    def get_profile(self) -> Dict[str, Any]:
        """Return the full profile."""
        return self.profile_data

    def update_interest(self, topic: str):
        """Add an interest if not present."""
        if topic not in self.profile_data["interests"]:
            self.profile_data["interests"].append(topic)
            self.save_profile()

    def update_preference(self, key: str, value: Any):
        """Update a preference."""
        self.profile_data["preferences"][key] = value
        self.save_profile()
