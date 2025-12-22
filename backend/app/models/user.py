"""
User Model for the Physical AI & Humanoid Robotics Platform
"""
from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class User:
    """
    User data model representing a registered user
    """
    id: str
    email: str
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        """Convert user object to dictionary"""
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Create User instance from dictionary"""
        return cls(
            id=data.get("id"),
            email=data.get("email"),
            is_active=data.get("is_active", True),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )


@dataclass
class UserCreate:
    """
    User creation model for registration
    """
    email: str
    password: str
    software_background: Optional[str] = None
    hardware_background: Optional[str] = None
    experience_level: Optional[str] = None
    programming_languages: Optional[str] = None
    learning_goals: Optional[str] = None


@dataclass
class UserUpdate:
    """
    User update model for profile updates
    """
    software_background: Optional[str] = None
    hardware_background: Optional[str] = None
    experience_level: Optional[str] = None
    programming_languages: Optional[str] = None
    learning_goals: Optional[str] = None