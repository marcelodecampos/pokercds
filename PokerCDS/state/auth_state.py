#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Authentication state management.
"""

import reflex as rx
from typing import Optional
from ..utils.timezone import now


class AuthState(rx.State):
    """Global authentication state."""
    
    # User session data
    user_id: Optional[int] = None
    user_name: str = ""
    user_nickname: str = ""
    user_email: str = ""
    is_admin: bool = False
    
    @rx.var
    def user_display_name(self) -> str:
        """Return nickname if available, otherwise return name."""
        return self.user_nickname if self.user_nickname else self.user_name
    
    @rx.var
    def user_display_initials(self) -> str:
        """Return initials for avatar display."""
        display = self.user_display_name
        return display[0].upper() if display else "U"
    
    @rx.var
    def can_edit_nickname(self) -> bool:
        """Return True if current user can edit nickname (only admins)."""
        return self.is_admin
    
    def login_user(self, user_data: dict):
        """Login user and set session data."""
        self.user_id = user_data.get("id")
        self.user_name = user_data.get("name", "")
        self.user_nickname = user_data.get("nickname", "")
        self.user_email = user_data.get("email", "")
        self.is_admin = user_data.get("is_admin", False)
        
    def logout_user(self):
        """Logout user and clear session data."""
        self.user_id = None
        self.user_name = ""
        self.user_nickname = ""
        self.user_email = ""
        self.is_admin = False
        return rx.redirect("/")

    def debug_print_state(self, more_info: str | None = ""):
        """Print all auth state variables for debugging."""
        current_time = now().strftime("%Y-%m-%d %H:%M:%S %Z")
        print(f"=== AUTH STATE DEBUG - {current_time} ==={more_info}")
        print(f"user_id: {self.user_id}")
        print(f"user_name: '{self.user_name}'")
        print(f"user_nickname: '{self.user_nickname}'")
        print(f"user_email: '{self.user_email}'")
        print(f"is_admin: {self.is_admin}")
        print(f"user_display_name: '{self.user_display_name}'")
        print(f"user_display_initials: '{self.user_display_initials}'")
        print("=" * 50)
        
    def require_auth(self):
        """Redirect to login if not authenticated."""
        if not self.user_id:
            return rx.redirect("/")
