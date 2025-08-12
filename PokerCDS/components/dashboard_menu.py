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
    """Dashboard menu with all available options."""
    return rx.vstack(
        rx.heading(
            "Menu Principal",
            size="6",
            margin_bottom="2rem",
            color="gray.800",
        ),
        
        # Main menu grid
        rx.grid(
            # Game-related options
            MenuCard(
                title="Meus Jogos",
                description="Visualizar histórico dos seus jogos e resultados",
                icon="dice-6",
                route="/my-games",
            ),
            MenuCard(
                title="Lista de Jogos",
                description="Ver todos os jogos e participantes",
                icon="list",
                route="/games-list",
            ),
            MenuCard(
                title="Resultados",
                description="Consultar resultados e estatísticas",
                icon="trophy",
                route="/results",
            ),
            
            # Admin-only options
            MenuCard(
                title="Gerenciar Membros",
                description="Cadastrar e gerenciar membros do grupo",
                icon="users",
                route="/members",
                admin_only=True,
            ),
            MenuCard(
                title="Novo Jogo",
                description="Iniciar uma nova sessão de poker",
                icon="plus-circle",
                route="/new-game",
                admin_only=True,
            ),
            MenuCard(
                title="Relatórios",
                description="Relatórios financeiros e estatísticas gerais",
                icon="bar-chart-3",
                route="/reports",
                admin_only=True,
            ),
            
            columns="3",
            gap="1.5rem",
            width="100%",
        ),
        
        spacing="4",
        align="center",
        width="100%",
    )
