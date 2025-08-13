#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Optional
from sqlmodel import Field
from sqlalchemy import Column, Integer, ForeignKey, Numeric
from decimal import Decimal
from .base import Base

# Constants
BUYIN_VALUE = Decimal('50.00')
MONEY_PRECISION = Numeric(12, 2)
ZERO_DECIMAL = Decimal('0.00')

class GameMember(Base, table=True):
    """Relationship table between Game and Member with poker session data."""
    
    __tablename__ = "game_members"
    game_id: int = Field(sa_column=Column(Integer, ForeignKey("games.id"), primary_key=True))
    member_id: int = Field(sa_column=Column(Integer, ForeignKey("members.id"), primary_key=True))
    
    # Poker session financial data
    credit_buyin: int = Field(default=0)  # Buy-ins on credit (integer count)
    cash_buyin: int = Field(default=0)  # Buy-ins with cash (integer count)
    final_chips: Decimal = Field(default=ZERO_DECIMAL, sa_column=Column(MONEY_PRECISION))  # Final chips value
    rango: Decimal = Field(default=ZERO_DECIMAL, sa_column=Column(MONEY_PRECISION))  # 5 reais ao final de cada jogador
    pingo: Decimal = Field(default=ZERO_DECIMAL, sa_column=Column(MONEY_PRECISION))  # resto menor que 10 reais de cada jogador
    received_amount: Decimal = Field(default=ZERO_DECIMAL, sa_column=Column(MONEY_PRECISION))  # Amount received
    
    @property
    def saldo_final(self) -> Decimal:
        """
        Calculated field for final balance.
        Formula: final_chips + received_amount - (credit_buyin + cash_buyin) * 50 - rango - pingo
        """
        total_amount = (
            (self.credit_buyin * -BUYIN_VALUE) +
            self.final_chips +
            self.rango +
            self.pingo -
            self.received_amount
        )
        return total_amount

