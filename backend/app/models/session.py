"""
Session Model for the Physical AI & Humanoid Robotics Platform
"""
from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Session:
    """
    Session data model representing an active user session
    """
    session_id: str
    user_id: str
    expires_at: datetime
    created_at: Optional[datetime] = None
    last_accessed: Optional[datetime] = None
    user_agent: Optional[str] = None
    ip_address: Optional[str] = None

    def is_expired(self) -> bool:
        """Check if the session has expired"""
        return datetime.utcnow() > self.expires_at

    def is_valid(self) -> bool:
        """Check if the session is valid (not expired and active)"""
        return not self.is_expired()

    def to_dict(self) -> dict:
        """Convert session object to dictionary"""
        return {
            "session_id": self.session_id,
            "user_id": self.user_id,
            "expires_at": self.expires_at.isoformat(),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_accessed": self.last_accessed.isoformat() if self.last_accessed else None,
            "user_agent": self.user_agent,
            "ip_address": self.ip_address
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Create Session instance from dictionary"""
        return cls(
            session_id=data.get("session_id"),
            user_id=data.get("user_id"),
            expires_at=datetime.fromisoformat(data["expires_at"]) if isinstance(data.get("expires_at"), str) else data.get("expires_at"),
            created_at=datetime.fromisoformat(data["created_at"]) if data.get("created_at") and isinstance(data.get("created_at"), str) else data.get("created_at"),
            last_accessed=datetime.fromisoformat(data["last_accessed"]) if data.get("last_accessed") and isinstance(data.get("last_accessed"), str) else data.get("last_accessed"),
            user_agent=data.get("user_agent"),
            ip_address=data.get("ip_address")
        )