#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Pages package for PokerCDS.

This package contains all page components for the application.
"""

from .login import login_page
from .dashboard import dashboard_page

__version__ = "1.0.0"
__all__ = ["login_page", "dashboard_page"]
