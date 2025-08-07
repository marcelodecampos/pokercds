#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Pages package for PokerCDS.

This package contains all page components for the application.
"""

from .login import login_page
from .profile import profile_page
from .change_password import change_password_page

__version__ = "1.0.0"
__all__ = ["login_page", "profile_page", "change_password_page"]
