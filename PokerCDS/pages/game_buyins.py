#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Game buyins management page for poker session financial control.
"""

import reflex as rx
import asyncio
from decimal import Decimal
from typing import List, Optional
from ..state.auth_state import AuthState


class GameBuyinsState(rx.State):
    """State for game buyins management."""
    
    # Game info
    current_game_id: Optional[int] = None
    game_date: str = ""
    game_description: str = ""
    
    # Players data
    players: List[dict] = []
    
    # Form fields for editing player
    editing_player_id: Optional[int] = None
    show_edit_modal: bool = False
    credit_buyin: int = 0
    cash_buyin: int = 0
    final_chips: str = "0.00"
    received_amount: str = "0.00"
    rango: str = "0.00"
    pingo: str = "0.00"
    
    # Loading states
    is_loading: bool = False
    is_saving: bool = False
    
    # Messages
    error_message: str = ""
    success_message: str = ""
    
    # Totals (calculated)
    total_credit_buyins: int = 0
    total_cash_buyins: int = 0
    total_final_chips: Decimal = Decimal('0.00')
    total_received: Decimal = Decimal('0.00')
    total_balance: Decimal = Decimal('0.00')
    
    @rx.var
    def total_balance_color(self) -> str:
        """Return color for total balance."""
        return "green.600" if float(self.total_balance) >= 0 else "red.600"
    
    async def load_game_data(self, game_id: int):
        """Load game and players data."""
        self.current_game_id = game_id
        self.is_loading = True
        self.error_message = ""
        
        try:
            # TODO: Replace with actual database query
            await asyncio.sleep(0.5)
            
            # Mock game data
            self.game_date = "24/04/2025"
            self.game_description = "Jogo de sexta-feira"
            
            # Mock players data based on the spreadsheet
            mock_players = [
                {
                    "id": 1,
                    "member_id": 1,
                    "name": "thats",
                    "credit_buyin": 2,
                    "cash_buyin": 0,
                    "final_chips": Decimal('140.00'),
                    "received_amount": Decimal('0.00'),
                    "rango": Decimal('0.00'),
                    "pingo": Decimal('0.00'),
                },
                {
                    "id": 2,
                    "member_id": 2,
                    "name": "didi",
                    "credit_buyin": 8,
                    "cash_buyin": 0,
                    "final_chips": Decimal('80.00'),
                    "received_amount": Decimal('0.00'),
                    "rango": Decimal('0.00'),
                    "pingo": Decimal('0.00'),
                },
                {
                    "id": 3,
                    "member_id": 3,
                    "name": "arrudao",
                    "credit_buyin": 3,
                    "cash_buyin": 0,
                    "final_chips": Decimal('0.00'),
                    "received_amount": Decimal('0.00'),
                    "rango": Decimal('0.00'),
                    "pingo": Decimal('0.00'),
                },
                {
                    "id": 4,
                    "member_id": 4,
                    "name": "jassa",
                    "credit_buyin": 1,
                    "cash_buyin": 0,
                    "final_chips": Decimal('100.00'),
                    "received_amount": Decimal('0.00'),
                    "rango": Decimal('0.00'),
                    "pingo": Decimal('0.00'),
                },
                {
                    "id": 5,
                    "member_id": 5,
                    "name": "pedrinho",
                    "credit_buyin": 0,
                    "cash_buyin": 2,
                    "final_chips": Decimal('280.00'),
                    "received_amount": Decimal('100.00'),
                    "rango": Decimal('0.00'),
                    "pingo": Decimal('0.00'),
                },
                {
                    "id": 6,
                    "member_id": 6,
                    "name": "vg",
                    "credit_buyin": 0,
                    "cash_buyin": 1,
                    "final_chips": Decimal('250.00'),
                    "received_amount": Decimal('50.00'),
                    "rango": Decimal('0.00'),
                    "pingo": Decimal('0.00'),
                },
            ]
            
            self.players = mock_players
            self._calculate_totals()
            
        except Exception as e:
            self.error_message = f"Erro ao carregar dados do jogo: {str(e)}"
            
        finally:
            self.is_loading = False
    
    def _calculate_totals(self):
        """Calculate totals for the game."""
        self.total_credit_buyins = sum(p["credit_buyin"] for p in self.players)
        self.total_cash_buyins = sum(p["cash_buyin"] for p in self.players)
        self.total_final_chips = sum(p["final_chips"] for p in self.players)
        self.total_received = sum(p["received_amount"] for p in self.players)
        
        # Calculate total balance (should be close to zero in a balanced game)
        total_buyins_value = (self.total_credit_buyins + self.total_cash_buyins) * Decimal('50.00')
        self.total_balance = self.total_final_chips + self.total_received - total_buyins_value
    
    def _calculate_player_balance(self, player: dict) -> Decimal:
        """Calculate individual player balance."""
        total_buyins = (player["credit_buyin"] + player["cash_buyin"]) * Decimal('50.00')
        return (
            player["final_chips"] + 
            player["rango"] + 
            player["pingo"] - 
            player["received_amount"] - 
            total_buyins
        )
    
    @rx.var
    def players_with_balance(self) -> List[dict]:
        """Return players with calculated balance."""
        result = []
        for player in self.players:
            player_copy = player.copy()
            total_buyins = (player["credit_buyin"] + player["cash_buyin"]) * 50.00
            balance = (
                float(player["final_chips"]) + 
                float(player["rango"]) + 
                float(player["pingo"]) - 
                float(player["received_amount"]) - 
                total_buyins
            )
            player_copy["calculated_balance"] = balance
            player_copy["balance_color"] = "green.600" if balance >= 0 else "red.600"
            result.append(player_copy)
        return result
    
    def open_edit_modal(self, player: dict):
        """Open edit modal for player."""
        self.editing_player_id = player["id"]
        self.credit_buyin = player["credit_buyin"]
        self.cash_buyin = player["cash_buyin"]
        self.final_chips = str(player["final_chips"])
        self.received_amount = str(player["received_amount"])
        self.rango = str(player["rango"])
        self.pingo = str(player["pingo"])
        self.show_edit_modal = True
    
    def close_edit_modal(self):
        """Close edit modal."""
        self.show_edit_modal = False
        self.editing_player_id = None
        self.credit_buyin = 0
        self.cash_buyin = 0
        self.final_chips = "0.00"
        self.received_amount = "0.00"
        self.rango = "0.00"
        self.pingo = "0.00"
    
    def set_credit_buyin(self, value: str):
        """Set credit buyin value."""
        try:
            self.credit_buyin = int(value) if value else 0
        except ValueError:
            self.credit_buyin = 0
    
    def set_cash_buyin(self, value: str):
        """Set cash buyin value."""
        try:
            self.cash_buyin = int(value) if value else 0
        except ValueError:
            self.cash_buyin = 0
    
    def set_final_chips(self, value: str):
        """Set final chips value."""
        self.final_chips = value
    
    def set_received_amount(self, value: str):
        """Set received amount value."""
        self.received_amount = value
    
    def set_rango(self, value: str):
        """Set rango value."""
        self.rango = value
    
    def set_pingo(self, value: str):
        """Set pingo value."""
        self.pingo = value
    
    def _validate_form(self) -> bool:
        """Validate form fields."""
        self.error_message = ""
        
        if self.credit_buyin < 0:
            self.error_message = "Cacifes a crédito não pode ser negativo"
            return False
        
        if self.cash_buyin < 0:
            self.error_message = "Cacifes em dinheiro não pode ser negativo"
            return False
        
        try:
            Decimal(self.final_chips)
            Decimal(self.received_amount)
            Decimal(self.rango)
            Decimal(self.pingo)
        except:
            self.error_message = "Valores monetários devem ser numéricos válidos"
            return False
        
        return True
    
    async def handle_save_player(self):
        """Save player data."""
        self.is_saving = True
        self.error_message = ""
        
        try:
            if not self._validate_form():
                return
            
            # TODO: Implement database update
            await asyncio.sleep(0.5)
            
            # Update player in local data
            for player in self.players:
                if player["id"] == self.editing_player_id:
                    player["credit_buyin"] = self.credit_buyin
                    player["cash_buyin"] = self.cash_buyin
                    player["final_chips"] = Decimal(self.final_chips)
                    player["received_amount"] = Decimal(self.received_amount)
                    player["rango"] = Decimal(self.rango)
                    player["pingo"] = Decimal(self.pingo)
                    break
            
            self._calculate_totals()
            self.success_message = "Dados do jogador atualizados com sucesso!"
            self.close_edit_modal()
            
        except Exception as e:
            self.error_message = f"Erro ao salvar dados: {str(e)}"
            
        finally:
            self.is_saving = False
    
    def clear_messages(self):
        """Clear error and success messages."""
        self.error_message = ""
        self.success_message = ""


def PlayersTable() -> rx.Component:
    """Table showing players and their buyins/results."""
    return rx.card(
        rx.vstack(
            # Table header with game info
            rx.hstack(
                rx.text(
                    f"Data: {GameBuyinsState.game_date}",
                    font_weight="bold",
                    size="4",
                    id="game-buyins-date",
                ),
                rx.text(
                    f"Descrição: {GameBuyinsState.game_description}",
                    size="3",
                    id="game-buyins-description",
                ),
                justify="between",
                width="100%",
                margin_bottom="1rem",
                id="game-buyins-header-info",
            ),
            
            # Table
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("Jogador", id="buyins-header-player"),
                        rx.table.column_header_cell("Cacifes Crédito", id="buyins-header-credit"),
                        rx.table.column_header_cell("Cacifes Dinheiro", id="buyins-header-cash"),
                        rx.table.column_header_cell("Fichas ao Final", id="buyins-header-chips"),
                        rx.table.column_header_cell("Recebido", id="buyins-header-received"),
                        rx.table.column_header_cell("Rango", id="buyins-header-rango"),
                        rx.table.column_header_cell("Pingo", id="buyins-header-pingo"),
                        rx.table.column_header_cell("Saldo Final", id="buyins-header-balance"),
                        rx.table.column_header_cell("Ações", id="buyins-header-actions"),
                        id="buyins-header-row",
                    ),
                    id="buyins-header-section",
                ),
                rx.table.body(
                    rx.foreach(
                        GameBuyinsState.players_with_balance,
                        lambda player: rx.table.row(
                            rx.table.cell(
                                player["name"],
                                font_weight="medium",
                                id=f"player-cell-name-{player['id']}",
                            ),
                            rx.table.cell(
                                player["credit_buyin"],
                                id=f"player-cell-credit-{player['id']}",
                            ),
                            rx.table.cell(
                                player["cash_buyin"],
                                id=f"player-cell-cash-{player['id']}",
                            ),
                            rx.table.cell(
                                f"R$ {player['final_chips']:.2f}",
                                id=f"player-cell-chips-{player['id']}",
                            ),
                            rx.table.cell(
                                f"R$ {player['received_amount']:.2f}",
                                id=f"player-cell-received-{player['id']}",
                            ),
                            rx.table.cell(
                                f"R$ {player['rango']:.2f}",
                                id=f"player-cell-rango-{player['id']}",
                            ),
                            rx.table.cell(
                                f"R$ {player['pingo']:.2f}",
                                id=f"player-cell-pingo-{player['id']}",
                            ),
                            rx.table.cell(
                                rx.text(
                                    f"R$ {player['calculated_balance']:.2f}",
                                    color=player["balance_color"],
                                    font_weight="bold",
                                    id=f"player-cell-balance-{player['id']}",
                                ),
                            ),
                            rx.table.cell(
                                rx.button(
                                    rx.icon("edit", size=14, id=f"player-edit-icon-{player['id']}"),
                                    on_click=lambda: GameBuyinsState.open_edit_modal(player),
                                    variant="ghost",
                                    size="1",
                                    id=f"player-edit-button-{player['id']}",
                                ),
                                id=f"player-cell-actions-{player['id']}",
                            ),
                            id=f"player-row-{player['id']}",
                        ),
                    ),
                    
                    # Totals row
                    rx.table.row(
                        rx.table.cell(
                            "TOTAL",
                            font_weight="bold",
                            id="totals-cell-label",
                        ),
                        rx.table.cell(
                            GameBuyinsState.total_credit_buyins,
                            font_weight="bold",
                            id="totals-cell-credit",
                        ),
                        rx.table.cell(
                            GameBuyinsState.total_cash_buyins,
                            font_weight="bold",
                            id="totals-cell-cash",
                        ),
                        rx.table.cell(
                            f"R$ {GameBuyinsState.total_final_chips:.2f}",
                            font_weight="bold",
                            id="totals-cell-chips",
                        ),
                        rx.table.cell(
                            f"R$ {GameBuyinsState.total_received:.2f}",
                            font_weight="bold",
                            id="totals-cell-received",
                        ),
                        rx.table.cell(
                            "R$ 0,00",
                            font_weight="bold",
                            id="totals-cell-rango",
                        ),
                        rx.table.cell(
                            "R$ 0,00",
                            font_weight="bold",
                            id="totals-cell-pingo",
                        ),
                        rx.table.cell(
                            rx.text(
                                f"R$ {GameBuyinsState.total_balance:.2f}",
                                font_weight="bold",
                                color=GameBuyinsState.total_balance_color,
                                id="totals-cell-balance",
                            ),
                        ),
                        rx.table.cell("", id="totals-cell-actions"),
                        style={"border-top": "2px solid var(--gray-6)"},
                        id="totals-row",
                    ),
                    
                    id="buyins-table-body",
                ),
                width="100%",
                id="buyins-table",
            ),
            
            width="100%",
            id="buyins-table-container",
        ),
        padding="1.5rem",
        width="100%",
        height="100%",
        id="buyins-table-card",
    )


def EditPlayerModal() -> rx.Component:
    """Modal for editing player data."""
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Editar Dados do Jogador", id="edit-player-modal-title"),
            rx.card(
                rx.vstack(
                    # Credit Buyins
                    rx.vstack(
                        rx.text("Cacifes a Crédito", size="3", font_weight="medium", id="edit-player-credit-label"),
                        rx.input(
                            type="number",
                            value=GameBuyinsState.credit_buyin,
                            on_change=GameBuyinsState.set_credit_buyin,
                            min="0",
                            size="3",
                            width="100%",
                            id="edit-player-credit-input",
                        ),
                        width="100%",
                        spacing="1",
                        id="edit-player-credit-field",
                    ),
                    
                    # Cash Buyins
                    rx.vstack(
                        rx.text("Cacifes em Dinheiro", size="3", font_weight="medium", id="edit-player-cash-label"),
                        rx.input(
                            type="number",
                            value=GameBuyinsState.cash_buyin,
                            on_change=GameBuyinsState.set_cash_buyin,
                            min="0",
                            size="3",
                            width="100%",
                            id="edit-player-cash-input",
                        ),
                        width="100%",
                        spacing="1",
                        id="edit-player-cash-field",
                    ),
                    
                    # Final Chips
                    rx.vstack(
                        rx.text("Fichas ao Final (R$)", size="3", font_weight="medium", id="edit-player-chips-label"),
                        rx.input(
                            type="number",
                            step="0.01",
                            value=GameBuyinsState.final_chips,
                            on_change=GameBuyinsState.set_final_chips,
                            min="0",
                            size="3",
                            width="100%",
                            id="edit-player-chips-input",
                        ),
                        width="100%",
                        spacing="1",
                        id="edit-player-chips-field",
                    ),
                    
                    # Received Amount
                    rx.vstack(
                        rx.text("Valor Recebido (R$)", size="3", font_weight="medium", id="edit-player-received-label"),
                        rx.input(
                            type="number",
                            step="0.01",
                            value=GameBuyinsState.received_amount,
                            on_change=GameBuyinsState.set_received_amount,
                            min="0",
                            size="3",
                            width="100%",
                            id="edit-player-received-input",
                        ),
                        width="100%",
                        spacing="1",
                        id="edit-player-received-field",
                    ),
                    
                    # Rango
                    rx.vstack(
                        rx.text("Rango (R$)", size="3", font_weight="medium", id="edit-player-rango-label"),
                        rx.input(
                            type="number",
                            step="0.01",
                            value=GameBuyinsState.rango,
                            on_change=GameBuyinsState.set_rango,
                            min="0",
                            size="3",
                            width="100%",
                            id="edit-player-rango-input",
                        ),
                        width="100%",
                        spacing="1",
                        id="edit-player-rango-field",
                    ),
                    
                    # Pingo
                    rx.vstack(
                        rx.text("Pingo (R$)", size="3", font_weight="medium", id="edit-player-pingo-label"),
                        rx.input(
                            type="number",
                            step="0.01",
                            value=GameBuyinsState.pingo,
                            on_change=GameBuyinsState.set_pingo,
                            min="0",
                            size="3",
                            width="100%",
                            id="edit-player-pingo-input",
                        ),
                        width="100%",
                        spacing="1",
                        id="edit-player-pingo-field",
                    ),
                    
                    # Error Message
                    rx.cond(
                        GameBuyinsState.error_message != "",
                        rx.text(
                            GameBuyinsState.error_message,
                            color="red.500",
                            size="2",
                            id="edit-player-error-message",
                        ),
                    ),
                    
                    # Buttons
                    rx.hstack(
                        rx.button(
                            "Cancelar",
                            variant="outline",
                            on_click=GameBuyinsState.close_edit_modal,
                            disabled=GameBuyinsState.is_saving,
                            id="edit-player-cancel-button",
                        ),
                        rx.button(
                            rx.cond(
                                GameBuyinsState.is_saving,
                                rx.hstack(
                                    rx.spinner(size="1", id="edit-player-loading-spinner"),
                                    rx.text("Salvando...", id="edit-player-loading-text"),
                                    spacing="2",
                                    id="edit-player-loading-content",
                                ),
                                rx.text("Salvar", id="edit-player-save-text"),
                            ),
                            on_click=GameBuyinsState.handle_save_player,
                            disabled=GameBuyinsState.is_saving,
                            id="edit-player-save-button",
                        ),
                        spacing="3",
                        justify="end",
                        width="100%",
                        id="edit-player-buttons",
                    ),
                    
                    spacing="4",
                    width="100%",
                    id="edit-player-form-content",
                ),
                padding="0",
                id="edit-player-form-card",
            ),
            max_width="500px",
            id="edit-player-modal-content",
        ),
        open=GameBuyinsState.show_edit_modal,
        id="edit-player-modal",
    )


@rx.page(route="/games/[game_id]/buyins", title="PokerCDS - Controle de Cacifes", on_load=GameBuyinsState.load_game_data)
def game_buyins_page() -> rx.Component:
    """Game buyins management page."""
    return rx.box(
        # Header
        rx.box(
            rx.container(
                rx.hstack(
                    rx.button(
                        rx.icon("arrow-left", size=16, id="buyins-back-icon"),
                        "Voltar",
                        variant="outline",
                        on_click=lambda: rx.redirect("/games"),
                        id="buyins-back-button",
                    ),
                    rx.heading("Controle de Cacifes", size="6", id="buyins-page-title"),
                    justify="between",
                    align="center",
                    width="100%",
                    id="buyins-header-content",
                ),
                max_width="1400px",
                id="buyins-header-container",
            ),
            padding="1.5rem 0",
            width="100%",
            id="buyins-header",
        ),
        
        # Main content
        rx.container(
            rx.vstack(
                # Messages
                rx.cond(
                    GameBuyinsState.error_message != "",
                    rx.callout(
                        GameBuyinsState.error_message,
                        icon="alert-circle",
                        color_scheme="red",
                        id="buyins-error-message",
                    ),
                ),
                rx.cond(
                    GameBuyinsState.success_message != "",
                    rx.callout(
                        GameBuyinsState.success_message,
                        icon="check-circle",
                        color_scheme="green",
                        id="buyins-success-message",
                    ),
                ),
                
                # Loading or table
                rx.cond(
                    GameBuyinsState.is_loading,
                    rx.center(
                        rx.vstack(
                            rx.spinner(size="3", id="buyins-loading-spinner"),
                            rx.text("Carregando dados...", id="buyins-loading-text"),
                            spacing="3",
                            align="center",
                            id="buyins-loading-content",
                        ),
                        padding="4rem",
                        id="buyins-loading-center",
                    ),
                    PlayersTable(),
                ),
                
                spacing="4",
                width="100%",
                id="buyins-main-content",
            ),
            max_width="1400px",
            padding="2rem",
            id="buyins-main-container",
        ),
        
        # Modals
        EditPlayerModal(),
        
        min_height="100vh",
        id="game-buyins-page",
    )
