#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
User profile component for dashboard header.
"""

import reflex as rx
from ..state.auth_state import AuthState


def UserProfile() -> rx.Component:
    """User profile component with dropdown menu."""
    return rx.hstack(
        # User avatar
        rx.box(
            rx.text(
                AuthState.user_display_initials,
                color="white",
                font_weight="bold",
                font_size="1.2rem",
            ),
            width="40px",
            height="40px",
            border_radius="50%",
            background="var(--accent-9)",  # Use theme accent color
            display="flex",
            align_items="center",
            justify_content="center",
        ),
        
        # User info and dropdown
        rx.vstack(
            rx.text(
                AuthState.user_display_name,
                font_weight="bold",
                font_size="0.9rem",
                color="var(--gray-12)",  # Theme-aware text color
            ),
            rx.text(
                rx.cond(
                    AuthState.is_admin,
                    "Administrador",
                    "Membro"
                ),
                font_size="0.8rem",
                color="var(--gray-11)",  # Theme-aware secondary text
            ),
            spacing="0",
            align_items="start",
        ),
        
        # Dropdown menu
        rx.menu.root(
            rx.menu.trigger(
                rx.icon("chevron-down", size=16, color="var(--gray-11)"),
            ),
            rx.menu.content(
                rx.menu.item(
                    rx.hstack(
                        rx.icon("user", size=16),
                        rx.text("Meus Dados"),
                        spacing="2",
                    ),
                    on_click=lambda: rx.redirect("/profile"),
                ),
                rx.menu.item(
                    rx.hstack(
                        rx.icon("key", size=16),
                        rx.text("Trocar Senha"),
                        spacing="2",
                    ),
                    on_click=lambda: rx.redirect("/change-password"),
                ),
                rx.menu.separator(),
                rx.menu.item(
                    rx.hstack(
                        rx.icon("log-out", size=16),
                        rx.text("Sair do Sistema"),
                        spacing="2",
                    ),
                    on_click=AuthState.logout_user,
                    color="red.600",
                ),
            ),
        ),
        
        spacing="3",
        align="center",
        padding="0.5rem",
        background="var(--gray-3)",  # Theme-aware card background
        border_radius="8px",
        box_shadow="0 2px 4px var(--shadow)",  # Theme-aware shadow
    )

