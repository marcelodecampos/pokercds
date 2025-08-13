#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Games management page with full CRUD operations.
"""

import reflex as rx
import asyncio
from datetime import date
from typing import List, Optional
from ..state.auth_state import AuthState


class GamesManagementState(rx.State):
    """State for games management page."""
    
    # Games list
    games: List[dict] = []
    selected_games: List[int] = []
    current_page: int = 1
    total_pages: int = 1
    games_per_page: int = 20
    
    # Modal states
    show_add_modal: bool = False
    show_edit_modal: bool = False
    show_delete_modal: bool = False
    editing_game: Optional[dict] = None
    
    # Form fields
    created_at: str = ""
    description: str = ""
    
    # Loading states
    is_loading: bool = False
    is_deleting: bool = False
    is_form_loading: bool = False
    
    # Messages
    error_message: str = ""
    success_message: str = ""
    
    async def load_games(self):
        """Load games from database (paginated, ordered by date desc)."""
        self.is_loading = True
        self.error_message = ""
        
        try:
            # TODO: Replace with actual database query
            # Simulate API call
            await asyncio.sleep(0.5)
            
            # Mock data for demonstration (ordered by date desc)
            mock_games = [
                {
                    "id": 3,
                    "created_at": "2024-01-15",
                    "description": "Jogo de domingo - Mesa cheia",
                },
                {
                    "id": 2,
                    "created_at": "2024-01-10",
                    "description": "Jogo da semana",
                },
                {
                    "id": 1,
                    "created_at": "2024-01-05",
                    "description": None,
                },
            ]
            
            self.games = mock_games
            self.total_pages = 1  # For now, single page
            
        except Exception as e:
            self.error_message = f"Erro ao carregar jogos: {str(e)}"
            
        finally:
            self.is_loading = False
    
    def set_created_at(self, value: str):
        """Set created_at value."""
        self.created_at = value
        
    def set_description(self, value: str):
        """Set description value."""
        self.description = value
    
    def toggle_game_selection(self, game_id: int):
        """Toggle game selection for bulk operations."""
        if game_id in self.selected_games:
            self.selected_games.remove(game_id)
        else:
            self.selected_games.append(game_id)
    
    def select_all_games(self):
        """Select all visible games."""
        self.selected_games = [game["id"] for game in self.games]
    
    def clear_selection(self):
        """Clear all selections."""
        self.selected_games = []
    
    def toggle_select_all(self):
        """Toggle select all games."""
        if len(self.selected_games) == len(self.games):
            self.clear_selection()
        else:
            self.select_all_games()
    
    def open_add_modal(self):
        """Open add game modal."""
        self.show_add_modal = True
        self.editing_game = None
        self.created_at = date.today().isoformat()
        self.description = ""
    
    def close_add_modal(self):
        """Close add game modal."""
        self.show_add_modal = False
        self.created_at = ""
        self.description = ""
    
    def open_edit_modal_by_id(self, game_id: int):
        """Open edit modal for specific game by ID."""
        game = next((g for g in self.games if g["id"] == game_id), None)
        if game:
            self.editing_game = game
            self.created_at = game["created_at"]
            self.description = game["description"] or ""
            self.show_edit_modal = True
    
    def close_edit_modal(self):
        """Close edit game modal."""
        self.show_edit_modal = False
        self.editing_game = None
        self.created_at = ""
        self.description = ""
    
    def open_delete_modal(self):
        """Open delete confirmation modal."""
        if self.selected_games:
            self.show_delete_modal = True
    
    def close_delete_modal(self):
        """Close delete confirmation modal."""
        self.show_delete_modal = False
    
    def delete_single_game(self, game_id: int):
        """Set single game for deletion and open modal."""
        self.selected_games = [game_id]
        self.show_delete_modal = True
    
    def _validate_form(self) -> bool:
        """Validate form fields."""
        self.error_message = ""
        
        if not self.created_at:
            self.error_message = "Data é obrigatória"
            return False
            
        return True
    
    async def handle_add_submit(self):
        """Handle add game form submission."""
        self.is_form_loading = True
        self.error_message = ""
        
        try:
            if not self._validate_form():
                return
            
            # TODO: Implement database insertion
            await asyncio.sleep(1)
            
            game_data = {
                "created_at": self.created_at,
                "description": self.description if self.description else None,
            }
            print(f"DEBUG: Adding game: {game_data}")
            
            self.success_message = "Jogo adicionado com sucesso!"
            self.close_add_modal()
            
            # Reload games list
            await self.load_games()
            
        except Exception as e:
            self.error_message = f"Erro ao adicionar jogo: {str(e)}"
            
        finally:
            self.is_form_loading = False
    
    async def handle_edit_submit(self):
        """Handle edit game form submission."""
        self.is_form_loading = True
        self.error_message = ""
        
        try:
            if not self._validate_form():
                return
            
            # TODO: Implement database update
            await asyncio.sleep(1)
            
            game_data = {
                "id": self.editing_game["id"],
                "created_at": self.created_at,
                "description": self.description if self.description else None,
            }
            print(f"DEBUG: Updating game: {game_data}")
            
            self.success_message = "Jogo atualizado com sucesso!"
            self.close_edit_modal()
            
            # Reload games list
            await self.load_games()
            
        except Exception as e:
            self.error_message = f"Erro ao atualizar jogo: {str(e)}"
            
        finally:
            self.is_form_loading = False
    
    async def delete_selected_games(self):
        """Delete selected games."""
        self.is_deleting = True
        self.error_message = ""
        
        try:
            # TODO: Implement actual database deletion
            await asyncio.sleep(1)
            
            # Remove from local list (simulate)
            self.games = [
                game for game in self.games 
                if game["id"] not in self.selected_games
            ]
            
            count = len(self.selected_games)
            self.success_message = f"{count} jogo(s) excluído(s) com sucesso!"
            self.selected_games = []
            self.close_delete_modal()
            
        except Exception as e:
            self.error_message = f"Erro ao excluir jogos: {str(e)}"
            
        finally:
            self.is_deleting = False
    
    def clear_messages(self):
        """Clear error and success messages."""
        self.error_message = ""
        self.success_message = ""


def GamesTable() -> rx.Component:
    """Games table with selection and actions."""
    return rx.card(
        rx.vstack(
            # Table header with actions
            rx.hstack(
                rx.hstack(
                    rx.checkbox(
                        checked=GamesManagementState.selected_games.length() == GamesManagementState.games.length(),
                        on_change=lambda _: GamesManagementState.toggle_select_all(),
                        id="games-select-all-checkbox",
                    ),
                    rx.text(
                        "Selecionar todos", 
                        size="2",
                        id="games-select-all-text",
                    ),
                    spacing="2",
                    align="center",
                    id="games-select-all-container",
                ),
                rx.hstack(
                    rx.button(
                        rx.icon("plus", size=16, id="games-add-icon"),
                        "Novo Jogo",
                        on_click=GamesManagementState.open_add_modal,
                        size="2",
                        id="games-add-button",
                    ),
                    rx.button(
                        rx.icon("trash-2", size=16, id="games-bulk-delete-icon"),
                        rx.text("Excluir (", GamesManagementState.selected_games.length(), ")", id="games-bulk-delete-text"),
                        on_click=GamesManagementState.open_delete_modal,
                        disabled=GamesManagementState.selected_games.length() == 0,
                        color_scheme="red",
                        variant="outline",
                        size="2",
                        id="games-bulk-delete-button",
                    ),
                    spacing="2",
                    id="games-action-buttons",
                ),
                justify="between",
                width="100%",
                margin_bottom="1rem",
                id="games-table-header",
            ),
            
            # Table
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("", id="games-table-header-checkbox"),
                        rx.table.column_header_cell("Data", id="games-table-header-date"),
                        rx.table.column_header_cell("Descrição", id="games-table-header-description"),
                        rx.table.column_header_cell("Ações", id="games-table-header-actions"),
                        id="games-table-header-row",
                    ),
                    id="games-table-header-section",
                ),
                rx.table.body(
                    rx.foreach(
                        GamesManagementState.games,
                        lambda game: rx.table.row(
                            rx.table.cell(
                                rx.checkbox(
                                    checked=GamesManagementState.selected_games.contains(game["id"]),
                                    on_change=lambda _: GamesManagementState.toggle_game_selection(game["id"]),
                                    id=f"game-checkbox-{game['id']}",
                                ),
                                id=f"game-cell-checkbox-{game['id']}",
                            ),
                            rx.table.cell(
                                game["created_at"],
                                id=f"game-cell-date-{game['id']}",
                            ),
                            rx.table.cell(
                                rx.cond(
                                    game["description"],
                                    rx.text(game["description"], id=f"game-text-description-{game['id']}"),
                                    rx.text("Sem descrição", size="2", color="gray.500", id=f"game-text-no-description-{game['id']}"),
                                ),
                                id=f"game-cell-description-{game['id']}",
                            ),
                            rx.table.cell(
                                rx.hstack(
                                    rx.button(
                                        rx.icon("users", size=14, id=f"game-players-icon-{game['id']}"),
                                        on_click=lambda: rx.redirect(f"/games/{game['id']}/buyins"),
                                        variant="ghost",
                                        size="1",
                                        color_scheme="blue",
                                        id=f"game-players-button-{game['id']}",
                                    ),
                                    rx.button(
                                        rx.icon("pencil", size=14, id=f"game-edit-icon-{game['id']}"),
                                        on_click=lambda: GamesManagementState.open_edit_modal_by_id(game["id"]),
                                        variant="ghost",
                                        size="1",
                                        id=f"game-edit-button-{game['id']}",
                                    ),
                                    rx.button(
                                        rx.icon("trash-2", size=14, id=f"game-delete-icon-{game['id']}"),
                                        on_click=lambda: GamesManagementState.delete_single_game(game["id"]),
                                        variant="ghost",
                                        size="1",
                                        color_scheme="red",
                                        id=f"game-delete-button-{game['id']}",
                                    ),
                                    spacing="2",
                                    id=f"game-actions-{game['id']}",
                                ),
                                id=f"game-cell-actions-{game['id']}",
                            ),
                            id=f"game-row-{game['id']}",
                        ),
                    ),
                    id="games-table-body",
                ),
                width="100%",
                id="games-table",
            ),
            
            width="100%",
            id="games-table-container",
        ),
        padding="1.5rem",
        width="100%",
        height="100%",
        id="games-table-card",
    )


def GameFormModal(title: str, is_edit: bool = False) -> rx.Component:
    """Modal for adding/editing game."""
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(title, id=f"{'edit' if is_edit else 'add'}-game-modal-title"),
            rx.card(
                rx.vstack(
                    # Date Field
                    rx.vstack(
                        rx.text("Data", size="3", font_weight="medium", id=f"{'edit' if is_edit else 'add'}-game-date-label"),
                        rx.input(
                            type="date",
                            value=GamesManagementState.created_at,
                            on_change=GamesManagementState.set_created_at,
                            size="3",
                            width="100%",
                            id=f"{'edit' if is_edit else 'add'}-game-date-input",
                        ),
                        width="100%",
                        spacing="1",
                        id=f"{'edit' if is_edit else 'add'}-game-date-field",
                    ),
                    
                    # Description Field
                    rx.vstack(
                        rx.text("Descrição", size="3", font_weight="medium", id=f"{'edit' if is_edit else 'add'}-game-description-label"),
                        rx.text_area(
                            placeholder="Descrição do jogo (opcional)",
                            value=GamesManagementState.description,
                            on_change=GamesManagementState.set_description,
                            size="3",
                            width="100%",
                            rows="3",
                            id=f"{'edit' if is_edit else 'add'}-game-description-input",
                        ),
                        width="100%",
                        spacing="1",
                        id=f"{'edit' if is_edit else 'add'}-game-description-field",
                    ),
                    
                    # Error Message
                    rx.cond(
                        GamesManagementState.error_message != "",
                        rx.text(
                            GamesManagementState.error_message,
                            color="red.500",
                            size="2",
                            id=f"{'edit' if is_edit else 'add'}-game-error-message",
                        ),
                    ),
                    
                    # Buttons
                    rx.hstack(
                        rx.button(
                            "Cancelar",
                            variant="outline",
                            on_click=GamesManagementState.close_edit_modal if is_edit else GamesManagementState.close_add_modal,
                            disabled=GamesManagementState.is_form_loading,
                            id=f"{'edit' if is_edit else 'add'}-game-cancel-button",
                        ),
                        rx.button(
                            rx.cond(
                                GamesManagementState.is_form_loading,
                                rx.hstack(
                                    rx.spinner(size="1", id=f"{'edit' if is_edit else 'add'}-game-loading-spinner"),
                                    rx.text("Salvando...", id=f"{'edit' if is_edit else 'add'}-game-loading-text"),
                                    spacing="2",
                                    id=f"{'edit' if is_edit else 'add'}-game-loading-content",
                                ),
                                rx.text("Salvar", id=f"{'edit' if is_edit else 'add'}-game-save-text"),
                            ),
                            on_click=GamesManagementState.handle_edit_submit if is_edit else GamesManagementState.handle_add_submit,
                            disabled=GamesManagementState.is_form_loading,
                            id=f"{'edit' if is_edit else 'add'}-game-save-button",
                        ),
                        spacing="3",
                        justify="end",
                        width="100%",
                        id=f"{'edit' if is_edit else 'add'}-game-buttons",
                    ),
                    
                    spacing="4",
                    width="100%",
                    id=f"{'edit' if is_edit else 'add'}-game-form-content",
                ),
                padding="0",
                id=f"{'edit' if is_edit else 'add'}-game-form-card",
            ),
            max_width="500px",
            id=f"{'edit' if is_edit else 'add'}-game-modal-content",
        ),
        open=GamesManagementState.show_edit_modal if is_edit else GamesManagementState.show_add_modal,
        id=f"{'edit' if is_edit else 'add'}-game-modal",
    )


def DeleteConfirmationModal() -> rx.Component:
    """Modal for delete confirmation."""
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Confirmar Exclusão", id="delete-games-modal-title"),
            rx.vstack(
                rx.text(
                    "Tem certeza que deseja excluir ",
                    GamesManagementState.selected_games.length(),
                    " jogo(s) selecionado(s)?",
                    size="3",
                    id="delete-games-modal-question",
                ),
                rx.text(
                    "Esta ação não pode ser desfeita.",
                    size="2",
                    color="red.500",
                    id="delete-games-modal-warning",
                ),
                rx.hstack(
                    rx.button(
                        "Cancelar",
                        variant="outline",
                        on_click=GamesManagementState.close_delete_modal,
                        disabled=GamesManagementState.is_deleting,
                        id="delete-games-modal-cancel-button",
                    ),
                    rx.button(
                        rx.cond(
                            GamesManagementState.is_deleting,
                            rx.hstack(
                                rx.spinner(size="1", id="delete-games-modal-spinner"),
                                rx.text("Excluindo...", id="delete-games-modal-loading-text"),
                                spacing="2",
                                id="delete-games-modal-loading",
                            ),
                            rx.text("Excluir", id="delete-games-modal-confirm-text"),
                        ),
                        on_click=GamesManagementState.delete_selected_games,
                        color_scheme="red",
                        disabled=GamesManagementState.is_deleting,
                        id="delete-games-modal-confirm-button",
                    ),
                    spacing="3",
                    justify="end",
                    width="100%",
                    id="delete-games-modal-buttons",
                ),
                spacing="4",
                width="100%",
                id="delete-games-modal-content",
            ),
            max_width="400px",
            id="delete-games-modal-dialog-content",
        ),
        open=GamesManagementState.show_delete_modal,
        id="delete-games-confirmation-modal",
    )


@rx.page(route="/games", title="PokerCDS - Gerenciar Jogos", on_load=[AuthState.require_auth, GamesManagementState.load_games])
def games_management_page() -> rx.Component:
    """Games management page."""
    return rx.box(
        # Header
        rx.box(
            rx.container(
                rx.hstack(
                    rx.button(
                        rx.icon("arrow-left", size=16, id="games-back-icon"),
                        "Voltar",
                        variant="outline",
                        on_click=lambda: rx.redirect("/dashboard"),
                        id="games-back-button",
                    ),
                    rx.heading("Gerenciar Jogos", size="6", id="games-page-title"),
                    justify="between",
                    align="center",
                    width="100%",
                    id="games-header-content",
                ),
                max_width="1200px",
                id="games-header-container",
            ),
            padding="1.5rem 0",
            width="100%",
            id="games-header",
        ),
        
        # Main content
        rx.container(
            rx.vstack(
                # Messages
                rx.cond(
                    GamesManagementState.error_message != "",
                    rx.callout(
                        GamesManagementState.error_message,
                        icon="alert-circle",
                        color_scheme="red",
                        id="games-error-message",
                    ),
                ),
                rx.cond(
                    GamesManagementState.success_message != "",
                    rx.callout(
                        GamesManagementState.success_message,
                        icon="check-circle",
                        color_scheme="green",
                        id="games-success-message",
                    ),
                ),
                
                # Loading or table
                rx.cond(
                    GamesManagementState.is_loading,
                    rx.center(
                        rx.vstack(
                            rx.spinner(size="3", id="games-loading-spinner"),
                            rx.text("Carregando jogos...", id="games-loading-text"),
                            spacing="3",
                            align="center",
                            id="games-loading-content",
                        ),
                        padding="4rem",
                        id="games-loading-center",
                    ),
                    GamesTable(),
                ),
                
                spacing="4",
                width="100%",
                id="games-main-content",
            ),
            max_width="1200px",
            padding="2rem",
            id="games-main-container",
        ),
        
        # Modals
        GameFormModal("Adicionar Novo Jogo", is_edit=False),
        GameFormModal("Editar Jogo", is_edit=True),
        DeleteConfirmationModal(),
        
        min_height="100vh",
        id="games-management-page",
    )
