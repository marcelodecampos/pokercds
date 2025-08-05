#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Login page for PokerCDS application.
"""

import reflex as rx
from ..components.login_form import LoginForm


@rx.page(route="/", title="PokerCDS - Login")
def login_page() -> rx.Component:
    """Login page component."""
    return rx.box(
        LoginForm(),
        width="100%",
        min_height="100vh",
        background="linear-gradient(135deg, var(--sand-2) 0%, var(--sand-3) 100%)",
    )
