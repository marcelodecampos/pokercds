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
                id="user-profile-initials",
            ),
            width="40px",
            height="40px",
            border_radius="50%",
            background="linear-gradient(45deg, #667eea, #764ba2)",
            display="flex",
            align_items="center",
            justify_content="center",
            id="user-profile-avatar",
        ),
        
        # User info and dropdown
        rx.vstack(
            rx.text(
                AuthState.user_display_name,
                font_weight="bold",
                font_size="0.9rem",
                color="var(--gray-12)",
                id="user-profile-name",
            ),
            rx.text(
                rx.cond(
                    AuthState.is_admin,
                    "Administrador",
                    "Membro"
                ),
                font_size="0.8rem",
                color="var(--gray-11)",
                id="user-profile-role",
            ),
            spacing="0",
            align_items="start",
            id="user-profile-info",
        ),
        
        # Dropdown menu
        rx.menu.root(
            rx.menu.trigger(
                rx.icon("chevron-down", size=16, color="var(--gray-11)", id="user-profile-dropdown-icon"),
                id="user-profile-dropdown-trigger",
            ),
            rx.menu.content(
                rx.menu.item(
                    rx.hstack(
                        rx.icon("user", size=16, id="user-profile-menu-profile-icon"),
                        rx.text("Meus Dados", id="user-profile-menu-profile-text"),
                        spacing="2",
                        id="user-profile-menu-profile-content",
                    ),
                    on_click=lambda: rx.redirect("/profile"),
                    id="user-profile-menu-profile",
                ),
                rx.menu.item(
                    rx.hstack(
                        rx.icon("key", size=16, id="user-profile-menu-password-icon"),
                        rx.text("Trocar Senha", id="user-profile-menu-password-text"),
                        spacing="2",
                        id="user-profile-menu-password-content",
                    ),
                    on_click=lambda: rx.redirect("/change-password"),
                    id="user-profile-menu-password",
                ),
                rx.menu.separator(id="user-profile-menu-separator"),
                rx.menu.item(
                    rx.hstack(
                        rx.icon("log-out", size=16, id="user-profile-menu-logout-icon"),
                        rx.text("Sair do Sistema", id="user-profile-menu-logout-text"),
                        spacing="2",
                        id="user-profile-menu-logout-content",
                    ),
                    on_click=AuthState.logout_user,
                    color="red.600",
                    id="user-profile-menu-logout",
                ),
                id="user-profile-menu-content",
            ),
            id="user-profile-dropdown",
        ),
        
        spacing="3",
        align="center",
        padding="0.5rem",
        background="var(--gray-3)",
        border_radius="8px",
        box_shadow="0 2px 4px var(--shadow)",
        id="user-profile-container",
    )

