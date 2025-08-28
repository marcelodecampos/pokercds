#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Game buyins management page for poker session financial control.
"""

import reflex as rx
from ..state.auth_state import AuthState
from ..state.game_buyins_state import GameBuyinsState


def PlayersTable() -> rx.Component:
    """Table showing players and their buyins."""
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
                        rx.table.column_header_cell("Jogador", width="15%", id="buyins-header-player"),
                        rx.table.column_header_cell(
                            rx.vstack(
                                rx.text("Cacifes", font_weight="bold", size="2"),
                                rx.text("Créd", size="1", opacity="0.8"),
                                spacing="0",
                                align="center",
                            ),
                            width="8%",
                            id="buyins-header-credit"
                        ),
                        rx.table.column_header_cell(
                            rx.vstack(
                                rx.text("Cacifes", font_weight="bold", size="2"),
                                rx.text("Dinh", size="1", opacity="0.8"),
                                spacing="0",
                                align="center",
                            ),
                            width="8%",
                            id="buyins-header-cash"
                        ),
                        rx.table.column_header_cell("Fichas Final", width="10%", text_align="right", id="buyins-header-chips"),
                        rx.table.column_header_cell("Rango", width="8%", text_align="right", id="buyins-header-rango"),
                        rx.table.column_header_cell("Pingo", width="8%", text_align="right", id="buyins-header-pingo"),
                        rx.table.column_header_cell("Recebido", width="9%", text_align="right", id="buyins-header-received"),
                        rx.table.column_header_cell("Saldo Final", width="10%", text_align="right", id="buyins-header-balance"),
                        id="buyins-header-row",
                    ),
                    id="buyins-header-section",
                ),
                rx.table.body(
                    rx.foreach(
                        GameBuyinsState.players_with_edit_states,
                        lambda player: rx.table.row(
                            rx.table.cell(
                                player["name"],
                                font_weight="medium",
                                id=f"player-cell-name-{player['id']}",
                            ),
                            rx.table.cell(
                                rx.hstack(
                                    rx.button(
                                        rx.icon("minus", size=12),
                                        on_click=lambda: GameBuyinsState.decrement_credit_buyin(player["id"]),
                                        variant="ghost",
                                        size="1",
                                        disabled=player["credit_buyin"] == 0,
                                        id=f"player-credit-minus-{player['id']}",
                                    ),
                                    rx.text(
                                        player["credit_buyin"],
                                        min_width="20px",
                                        text_align="center",
                                        font_weight="medium",
                                        id=f"player-credit-value-{player['id']}",
                                    ),
                                    rx.button(
                                        rx.icon("plus", size=12),
                                        on_click=lambda: GameBuyinsState.increment_credit_buyin(player["id"]),
                                        variant="ghost",
                                        size="1",
                                        id=f"player-credit-plus-{player['id']}",
                                    ),
                                    spacing="1",
                                    align="center",
                                    justify="center",
                                ),
                                text_align="center",
                                id=f"player-cell-credit-{player['id']}",
                            ),
                            rx.table.cell(
                                rx.hstack(
                                    rx.button(
                                        rx.icon("minus", size=12),
                                        on_click=lambda: GameBuyinsState.decrement_cash_buyin(player["id"]),
                                        variant="ghost",
                                        size="1",
                                        disabled=player["cash_buyin"] == 0,
                                        id=f"player-cash-minus-{player['id']}",
                                    ),
                                    rx.text(
                                        player["cash_buyin"],
                                        min_width="20px",
                                        text_align="center",
                                        font_weight="medium",
                                        id=f"player-cash-value-{player['id']}",
                                    ),
                                    rx.button(
                                        rx.icon("plus", size=12),
                                        on_click=lambda: GameBuyinsState.increment_cash_buyin(player["id"]),
                                        variant="ghost",
                                        size="1",
                                        id=f"player-cash-plus-{player['id']}",
                                    ),
                                    spacing="1",
                                    align="center",
                                    justify="center",
                                ),
                                text_align="center",
                                id=f"player-cell-cash-{player['id']}",
                            ),
                            # Final Chips - Editable
                            rx.table.cell(
                                rx.cond(
                                    player["editing_final_chips"],
                                    rx.hstack(
                                        rx.input(
                                            type="number",
                                            step="0.01",
                                            value=GameBuyinsState.editing_value,
                                            on_change=GameBuyinsState.set_editing_value,
                                            on_key_down=lambda key: rx.cond(
                                                key == "Enter",
                                                GameBuyinsState.save_inline_edit(player["id"], "final_chips"),
                                                rx.cond(
                                                    key == "Escape",
                                                    GameBuyinsState.cancel_inline_edit(),
                                                    rx.noop()
                                                )
                                            ),
                                            size="1",
                                            width="80px",
                                            auto_focus=True,
                                            id=f"edit-final-chips-{player['id']}",
                                        ),
                                        rx.button(
                                            rx.icon("check", size=10),
                                            on_click=lambda: GameBuyinsState.save_inline_edit(player["id"], "final_chips"),
                                            variant="ghost",
                                            size="1",
                                            id=f"save-final-chips-{player['id']}",
                                        ),
                                        spacing="1",
                                        align="center",
                                        justify="end",
                                    ),
                                    rx.text(
                                        f"R$ {player['final_chips']:.2f}",
                                        on_click=lambda: GameBuyinsState.start_inline_edit(
                                            player["id"], "final_chips", str(player["final_chips"])
                                        ),
                                        cursor="pointer",
                                        _hover={"background": "gray.100"},
                                        padding="2px 4px",
                                        border_radius="2px",
                                        id=f"final-chips-text-{player['id']}",
                                    ),
                                ),
                                text_align="right",
                                id=f"player-cell-chips-{player['id']}",
                            ),
                            
                            # Rango - Editable
                            rx.table.cell(
                                rx.cond(
                                    player["editing_rango"],
                                    rx.hstack(
                                        rx.input(
                                            type="number",
                                            step="0.01",
                                            value=GameBuyinsState.editing_value,
                                            on_change=GameBuyinsState.set_editing_value,
                                            on_key_down=lambda key: rx.cond(
                                                key == "Enter",
                                                GameBuyinsState.save_inline_edit(player["id"], "rango"),
                                                rx.cond(
                                                    key == "Escape",
                                                    GameBuyinsState.cancel_inline_edit(),
                                                    rx.noop()
                                                )
                                            ),
                                            size="1",
                                            width="70px",
                                            auto_focus=True,
                                            id=f"edit-rango-{player['id']}",
                                        ),
                                        rx.button(
                                            rx.icon("check", size=10),
                                            on_click=lambda: GameBuyinsState.save_inline_edit(player["id"], "rango"),
                                            variant="ghost",
                                            size="1",
                                            id=f"save-rango-{player['id']}",
                                        ),
                                        spacing="1",
                                        align="center",
                                        justify="end",
                                    ),
                                    rx.text(
                                        f"R$ {player['rango']:.2f}",
                                        on_click=lambda: GameBuyinsState.start_inline_edit(
                                            player["id"], "rango", str(player["rango"])
                                        ),
                                        cursor="pointer",
                                        _hover={"background": "gray.100"},
                                        padding="2px 4px",
                                        border_radius="2px",
                                        id=f"rango-text-{player['id']}",
                                    ),
                                ),
                                text_align="right",
                                id=f"player-cell-rango-{player['id']}",
                            ),
                            
                            # Pingo - Editable
                            rx.table.cell(
                                rx.cond(
                                    player["editing_pingo"],
                                    rx.hstack(
                                        rx.input(
                                            type="number",
                                            step="0.01",
                                            value=GameBuyinsState.editing_value,
                                            on_change=GameBuyinsState.set_editing_value,
                                            on_key_down=lambda key: rx.cond(
                                                key == "Enter",
                                                GameBuyinsState.save_inline_edit(player["id"], "pingo"),
                                                rx.cond(
                                                    key == "Escape",
                                                    GameBuyinsState.cancel_inline_edit(),
                                                    rx.noop()
                                                )
                                            ),
                                            size="1",
                                            width="70px",
                                            auto_focus=True,
                                            id=f"edit-pingo-{player['id']}",
                                        ),
                                        rx.button(
                                            rx.icon("check", size=10),
                                            on_click=lambda: GameBuyinsState.save_inline_edit(player["id"], "pingo"),
                                            variant="ghost",
                                            size="1",
                                            id=f"save-pingo-{player['id']}",
                                        ),
                                        spacing="1",
                                        align="center",
                                        justify="end",
                                    ),
                                    rx.text(
                                        f"R$ {player['pingo']:.2f}",
                                        on_click=lambda: GameBuyinsState.start_inline_edit(
                                            player["id"], "pingo", str(player["pingo"])
                                        ),
                                        cursor="pointer",
                                        _hover={"background": "gray.100"},
                                        padding="2px 4px",
                                        border_radius="2px",
                                        id=f"pingo-text-{player['id']}",
                                    ),
                                ),
                                text_align="right",
                                id=f"player-cell-pingo-{player['id']}",
                            ),
                            
                            # Received Amount - Editable
                            rx.table.cell(
                                rx.cond(
                                    player["editing_received_amount"],
                                    rx.hstack(
                                        rx.input(
                                            type="number",
                                            step="0.01",
                                            value=GameBuyinsState.editing_value,
                                            on_change=GameBuyinsState.set_editing_value,
                                            on_key_down=lambda key: rx.cond(
                                                key == "Enter",
                                                GameBuyinsState.save_inline_edit(player["id"], "received_amount"),
                                                rx.cond(
                                                    key == "Escape",
                                                    GameBuyinsState.cancel_inline_edit(),
                                                    rx.noop()
                                                )
                                            ),
                                            size="1",
                                            width="80px",
                                            auto_focus=True,
                                            id=f"edit-received-{player['id']}",
                                        ),
                                        rx.button(
                                            rx.icon("check", size=10),
                                            on_click=lambda: GameBuyinsState.save_inline_edit(player["id"], "received_amount"),
                                            variant="ghost",
                                            size="1",
                                            id=f"save-received-{player['id']}",
                                        ),
                                        spacing="1",
                                        align="center",
                                        justify="end",
                                    ),
                                    rx.text(
                                        f"R$ {player['received_amount']:.2f}",
                                        on_click=lambda: GameBuyinsState.start_inline_edit(
                                            player["id"], "received_amount", str(player["received_amount"])
                                        ),
                                        cursor="pointer",
                                        _hover={"background": "gray.100"},
                                        padding="2px 4px",
                                        border_radius="2px",
                                        id=f"received-text-{player['id']}",
                                    ),
                                ),
                                text_align="right",
                                id=f"player-cell-received-{player['id']}",
                            ),
                            rx.table.cell(
                                rx.text(
                                    f"R$ {player['calculated_balance']:.2f}",
                                    color=player["balance_color"],
                                    font_weight="bold",
                                    text_align="right",
                                    id=f"player-cell-balance-{player['id']}",
                                ),
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
                            text_align="center",
                            id="totals-cell-credit",
                        ),
                        rx.table.cell(
                            GameBuyinsState.total_cash_buyins,
                            font_weight="bold",
                            text_align="center",
                            id="totals-cell-cash",
                        ),
                        rx.table.cell(
                            f"R$ {GameBuyinsState.total_final_chips:.2f}",
                            font_weight="bold",
                            text_align="right",
                            id="totals-cell-chips",
                        ),
                        rx.table.cell(
                            "",
                            id="totals-cell-rango",
                        ),
                        rx.table.cell(
                            "",
                            id="totals-cell-pingo",
                        ),
                        rx.table.cell(
                            "",
                            id="totals-cell-received",
                        ),
                        rx.table.cell(
                            rx.text(
                                f"R$ {GameBuyinsState.total_balance:.2f}",
                                font_weight="bold",
                                color=GameBuyinsState.total_balance_color,
                                text_align="right",
                                id="totals-cell-balance",
                            ),
                        ),
                        style={"border-top": "2px solid var(--gray-6)"},
                        id="totals-row",
                    ),
                    
                    # Values row (cacifes * 50)
                    rx.table.row(
                        rx.table.cell(
                            "VALOR R$",
                            font_weight="bold",
                            color="blue.600",
                            id="values-cell-label",
                        ),
                        rx.table.cell(
                            f"{GameBuyinsState.total_credit_buyins * 50:.2f}",
                            font_weight="bold",
                            color="blue.600",
                            text_align="center",
                            id="values-cell-credit",
                        ),
                        rx.table.cell(
                            f"{GameBuyinsState.total_cash_buyins * 50:.2f}",
                            font_weight="bold",
                            color="blue.600",
                            text_align="center",
                            id="values-cell-cash",
                        ),
                        rx.table.cell(
                            rx.text(
                                f"{GameBuyinsState.chips_difference_value:.2f}",
                                font_weight="bold",
                                color=GameBuyinsState.chips_difference_color,
                                text_align="right",
                                id="values-cell-chips-diff",
                            ),
                            id="values-cell-chips"
                        ),
                        rx.table.cell("", id="values-cell-rango"),
                        rx.table.cell("", id="values-cell-pingo"),
                        rx.table.cell("", id="values-cell-received"),
                        rx.table.cell("", id="values-cell-balance"),
                        id="values-row",
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

