#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Game buyins state management.
"""

import reflex as rx
import asyncio
from decimal import Decimal
from typing import List, Optional


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
    
    # Inline editing states
    editing_cell: str = ""  # Format: "player_id:field_name"
    editing_value: str = ""
    
    @rx.var
    def total_balance_color(self) -> str:
        """Return color for total balance."""
        return "green" if float(self.total_balance) >= 0 else "red"
    
    @rx.var
    def chips_difference_color(self) -> str:
        """Return color for chips difference calculation."""
        chips_difference = self.chips_difference_value
        color = "red" if float(chips_difference) < 0 else "blue"
        print (f"Color: {color}")
        return color

    @rx.var
    def chips_difference_value(self) -> Decimal:
        """Calculate chips difference: (total cred + total cash) * 50 - total final chips."""
        total_buyins_value = (self.total_credit_buyins + self.total_cash_buyins) * Decimal('50.00')
        return total_buyins_value - self.total_final_chips

    @rx.var
    def players_with_edit_states(self) -> List[dict]:
        """Return players with calculated balance and edit states."""
        result = []
        for player in self.players:
            player_copy = player.copy()
            total_buyins = player["credit_buyin"] * 50.00
            balance = (
                float(player["final_chips"]) + 
                float(player["rango"]) + 
                float(player["pingo"]) - 
                float(player["received_amount"]) - 
                total_buyins
            )
            player_copy["calculated_balance"] = balance
            player_copy["balance_color"] = "green.600" if balance >= 0 else "red.600"
            
            # Add edit states for each field
            player_id = player["id"]
            player_copy["editing_final_chips"] = self.editing_cell == f"{player_id}:final_chips"
            player_copy["editing_rango"] = self.editing_cell == f"{player_id}:rango"
            player_copy["editing_pingo"] = self.editing_cell == f"{player_id}:pingo"
            player_copy["editing_received_amount"] = self.editing_cell == f"{player_id}:received_amount"
            
            result.append(player_copy)
        return result
    
    async def load_game_data(self):
        """Load game and players data using router state."""
        # Get game_id from router
        game_id = self.router.page.params.get("game_id")
        if not game_id:
            self.error_message = "ID do jogo não encontrado"
            self.is_loading = False
            return
            
        try:
            game_id = int(game_id)
        except (ValueError, TypeError):
            self.error_message = "ID do jogo inválido"
            self.is_loading = False
            return
            
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
        total_rango = sum(p["rango"] for p in self.players)
        total_pingo = sum(p["pingo"] for p in self.players)
        self.total_credit_buyins = sum(p["credit_buyin"] for p in self.players)
        self.total_cash_buyins = sum(p["cash_buyin"] for p in self.players)
        self.total_final_chips = sum(p["final_chips"] for p in self.players) + total_rango + total_pingo
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
    
    async def increment_credit_buyin(self, player_id: int):
        """Increment credit buyin for a player."""
        for player in self.players:
            if player["id"] == player_id:
                player["credit_buyin"] += 1
                break
        self._calculate_totals()
        
    async def decrement_credit_buyin(self, player_id: int):
        """Decrement credit buyin for a player."""
        for player in self.players:
            if player["id"] == player_id:
                if player["credit_buyin"] > 0:
                    player["credit_buyin"] -= 1
                break
        self._calculate_totals()
        
    async def increment_cash_buyin(self, player_id: int):
        """Increment cash buyin for a player."""
        for player in self.players:
            if player["id"] == player_id:
                player["cash_buyin"] += 1
                break
        self._calculate_totals()
        
    async def decrement_cash_buyin(self, player_id: int):
        """Decrement cash buyin for a player."""
        for player in self.players:
            if player["id"] == player_id:
                if player["cash_buyin"] > 0:
                    player["cash_buyin"] -= 1
                break
        self._calculate_totals()
    
    def clear_messages(self):
        """Clear error and success messages."""
        self.error_message = ""
        self.success_message = ""
    
    def start_inline_edit(self, player_id: int, field_name: str, current_value: str):
        """Start inline editing for a cell."""
        self.editing_cell = f"{player_id}:{field_name}"
        self.editing_value = str(current_value)
    
    def cancel_inline_edit(self):
        """Cancel inline editing."""
        self.editing_cell = ""
        self.editing_value = ""
    
    def set_editing_value(self, value: str):
        """Set the value being edited."""
        self.editing_value = value
    
    async def save_inline_edit(self, player_id: int, field_name: str):
        """Save inline edit."""
        try:
            # Validate the value
            if field_name in ["final_chips", "received_amount", "rango", "pingo"]:
                decimal_value = Decimal(self.editing_value)
                if decimal_value < 0:
                    self.error_message = "Valor não pode ser negativo"
                    return
            
            # Update the player data
            for player in self.players:
                if player["id"] == player_id:
                    if field_name in ["final_chips", "received_amount", "rango", "pingo"]:
                        player[field_name] = Decimal(self.editing_value)
                    break
            
            # Recalculate totals
            self._calculate_totals()
            
            # Clear editing state
            self.editing_cell = ""
            self.editing_value = ""
            
        except (ValueError, TypeError):
            self.error_message = "Valor inválido"
