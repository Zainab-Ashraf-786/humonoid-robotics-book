"""
UserProfile Model for the Physical AI & Humanoid Robotics Platform
"""
from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class UserProfile:
    """
    User Profile data model containing user background information for personalization
    """
    user_id: str
    software_background: Optional[str] = None
    hardware_background: Optional[str] = None
    experience_level: Optional[str] = None  # beginner, intermediate, advanced
    programming_languages: Optional[str] = None
    learning_goals: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        """Convert user profile object to dictionary"""
        return {
            "user_id": self.user_id,
            "software_background": self.software_background,
            "hardware_background": self.hardware_background,
            "experience_level": self.experience_level,
            "programming_languages": self.programming_languages,
            "learning_goals": self.learning_goals,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Create UserProfile instance from dictionary"""
        return cls(
            user_id=data.get("user_id"),
            software_background=data.get("software_background"),
            hardware_background=data.get("hardware_background"),
            experience_level=data.get("experience_level"),
            programming_languages=data.get("programming_languages"),
            learning_goals=data.get("learning_goals"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )

    def get_personalization_context(self) -> dict:
        """
        Get a context dictionary for personalizing content based on user profile
        """
        return {
            "experience_level": self.experience_level or "beginner",
            "software_background": self.software_background or "general",
            "hardware_background": self.hardware_background or "general",
            "programming_languages": self.programming_languages or "not specified",
            "learning_goals": self.learning_goals or "general learning"
        }