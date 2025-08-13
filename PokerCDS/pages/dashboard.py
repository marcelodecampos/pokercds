#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Main dashboard page after login.
"""

import reflex as rx
from ..components.user_profile import UserProfile
from ..components.dashboard_menu import DashboardMenu
from ..state.auth_state import AuthState


@rx.page(route="/dashboard", title="PokerCDS - Dashboard", on_load=AuthState.require_auth)
def dashboard_page() -> rx.Component:
    """Main dashboard page."""
    return rx.box(
        # Header
        rx.box(
            rx.container(
                rx.hstack(
                    # Logo and title
                    rx.hstack(
                        rx.heading("PokerCDS", size="7", id="dashboard-logo"),
                        rx.text(
                            "Sistema de Controle Financeiro",
                            opacity="0.9",
                            font_size="0.9rem",
                            id="dashboard-subtitle",
                        ),
                        spacing="3",
                        align="center",
                        id="dashboard-logo-section",
                    ),
                    
                    # User profile
                    UserProfile(),
                    
                    justify="between",
                    align="center",
                    width="100%",
                    id="dashboard-header-content",
                ),
                max_width="1200px",
                id="dashboard-header-container",
            ),
            padding="1.5rem 0",
            width="100%",
            id="dashboard-header",
        ),
        
        # Main content
        rx.container(
            rx.vstack(
                # Welcome message
                rx.box(
                    rx.vstack(
                        rx.text(
                            f"Bem-vindo, {AuthState.user_nickname}!",
                            font_size="1.5rem",
                            font_weight="bold",
                            id="dashboard-welcome-name",
                        ),
                        rx.text(
                            rx.cond(
                                AuthState.is_admin,
                                "Você possui privilégios de administrador",
                                "Selecione uma opção abaixo para continuar",
                            ),
                            id="dashboard-welcome-message",
                        ),
                        spacing="1",
                        align="center",
                        id="dashboard-welcome-content",
                    ),
                    text_align="center",
                    margin_bottom="3rem",
                    padding="2rem",
                    border_radius="12px",
                    id="dashboard-welcome-box",
                ),
                
                # Dashboard menu
                DashboardMenu(),
                
                spacing="4",
                width="100%",
                id="dashboard-main-content",
            ),
            max_width="1200px",
            padding="2rem",
            id="dashboard-main-container",
        ),
        
        min_height="100vh",
        id="dashboard-page",
    )
