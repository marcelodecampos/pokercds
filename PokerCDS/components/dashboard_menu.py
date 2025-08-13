#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Dashboard menu component with navigation options.
"""

import reflex as rx
from ..state.auth_state import AuthState


def MenuCard(title: str, description: str, icon: str, route: str, admin_only: bool = False) -> rx.Component:
    """Menu card component."""
    return rx.cond(
        ~admin_only | AuthState.is_admin,
        rx.card(
            rx.vstack(
                rx.hstack(
                    rx.icon(icon, size=24, color="blue.600"),
                    rx.heading(title, size="4", color="gray.800"),
                    spacing="2",
                    align="center",
                ),
                rx.text(
                    description,
                    color="gray.600",
                    font_size="0.9rem",
                    text_align="center",
                ),
                spacing="3",
                align="center",
            ),
            padding="1.5rem",
            cursor="pointer",
            transition="all 0.2s",
            _hover={
                "transform": "translateY(-2px)",
                "box_shadow": "0 4px 12px rgba(0,0,0,0.15)",
            },
            on_click=lambda: rx.redirect(route),
        ),
    )


def DashboardMenu() -> rx.Component:
    """Dashboard menu with navigation cards."""
    return rx.vstack(
        # Admin section
        rx.cond(
            AuthState.is_admin,
            rx.vstack(
                rx.text(
                    "Administração", 
                    size="5", 
                    font_weight="bold", 
                    margin_bottom="1rem",
                    id="dashboard-menu-admin-title",
                ),
                rx.grid(
                    # Manage Members Card
                    rx.card(
                        rx.vstack(
                            rx.icon("users", size=32, id="dashboard-menu-manage-icon"),
                            rx.text(
                                "Gerenciar Membros", 
                                font_weight="bold", 
                                size="4",
                                id="dashboard-menu-manage-title",
                            ),
                            rx.text(
                                "Visualizar e editar membros", 
                                size="2", 
                                text_align="center",
                                id="dashboard-menu-manage-description",
                            ),
                            spacing="3",
                            align="center",
                            id="dashboard-menu-manage-content",
                        ),
                        on_click=lambda: rx.redirect("/members"),
                        style={"cursor": "pointer", "_hover": {"transform": "scale(1.02)"}},
                        padding="2rem",
                        id="dashboard-menu-manage-card",
                    ),
                    
                    # Manage Games Card
                    rx.card(
                        rx.vstack(
                            rx.icon("calendar", size=32, id="dashboard-menu-games-icon"),
                            rx.text(
                                "Gerenciar Jogos", 
                                font_weight="bold", 
                                size="4",
                                id="dashboard-menu-games-title",
                            ),
                            rx.text(
                                "Visualizar e editar jogos", 
                                size="2", 
                                text_align="center",
                                id="dashboard-menu-games-description",
                            ),
                            spacing="3",
                            align="center",
                            id="dashboard-menu-games-content",
                        ),
                        on_click=lambda: rx.redirect("/games"),
                        style={"cursor": "pointer", "_hover": {"transform": "scale(1.02)"}},
                        padding="2rem",
                        id="dashboard-menu-games-card",
                    ),
                    
                    columns="2",
                    spacing="4",
                    width="100%",
                    id="dashboard-menu-admin-grid",
                ),

                spacing="3",
                width="100%",
                margin_bottom="3rem",
                id="dashboard-menu-admin-section",
            ),
        ),
        
        # General section
        rx.text(
            "Funcionalidades", 
            size="5", 
            font_weight="bold", 
            margin_bottom="1rem",
            id="dashboard-menu-general-title",
        ),
        rx.grid(
            # Profile Card
            rx.card(
                rx.vstack(
                    rx.icon("user", size=32, id="dashboard-menu-profile-icon"),
                    rx.text(
                        "Meu Perfil", 
                        font_weight="bold", 
                        size="4",
                        id="dashboard-menu-profile-title",
                    ),
                    rx.text(
                        "Visualizar e editar meus dados", 
                        size="2", 
                        text_align="center",
                        id="dashboard-menu-profile-description",
                    ),
                    spacing="3",
                    align="center",
                    id="dashboard-menu-profile-content",
                ),
                on_click=lambda: rx.redirect("/profile"),
                style={"cursor": "pointer", "_hover": {"transform": "scale(1.02)"}},
                padding="2rem",
                id="dashboard-menu-profile-card",
            ),
            
            # Change Password Card
            rx.card(
                rx.vstack(
                    rx.icon("key", size=32, id="dashboard-menu-password-icon"),
                    rx.text(
                        "Trocar Senha", 
                        font_weight="bold", 
                        size="4",
                        id="dashboard-menu-password-title",
                    ),
                    rx.text(
                        "Alterar minha senha de acesso", 
                        size="2", 
                        text_align="center",
                        id="dashboard-menu-password-description",
                    ),
                    spacing="3",
                    align="center",
                    id="dashboard-menu-password-content",
                ),
                on_click=lambda: rx.redirect("/change-password"),
                style={"cursor": "pointer", "_hover": {"transform": "scale(1.02)"}},
                padding="2rem",
                id="dashboard-menu-password-card",
            ),
            
            columns="2",
            spacing="4",
            width="100%",
            id="dashboard-menu-general-grid",
        ),
        
        spacing="4",
        width="100%",
        id="dashboard-menu-container",
    )
