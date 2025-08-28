#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
User data models for type safety and consistency.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class UserData:
    """User data model for authentication and session management."""
    
    id: int
    name: str
    nickname: Optional[str] = None
    email: Optional[str] = None
    is_admin: bool = False
    is_enabled: bool = True
    
    @property
    def display_name(self) -> str:
        """Return nickname if available, otherwise return name."""
        return self.nickname if self.nickname else self.name
    
    @property
    def display_initials(self) -> str:
        """Return initials for avatar display."""
        display = self.display_name
        return display[0].upper() if display else "U"
    
    def to_dict(self) -> dict:
        """Convert to dictionary for compatibility with existing code."""
        return {
            "id": self.id,
            "name": self.name,
            "nickname": self.nickname,
            "email": self.email,
            "is_admin": self.is_admin,
            "is_enabled": self.is_enabled,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "UserData":
        """Create UserData from dictionary."""
        return cls(
            id=data["id"],
            name=data["name"],
            nickname=data.get("nickname"),
            email=data.get("email"),
            is_admin=data.get("is_admin", False),
            is_enabled=data.get("is_enabled", True),
        )
