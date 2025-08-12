#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Pages package for PokerCDS.

This package contains all page components for the application.
"""

from .login import login_page
from .profile import profile_page
from .change_password import change_password_page
from .member_registration import member_registration_page
from .members_management import members_management_page

__version__ = "1.0.0"
__all__ = ["login_page", "profile_page", "change_password_page", "member_registration_page", "members_management_page"]
