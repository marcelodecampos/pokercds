#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import date
from typing import Optional
from sqlmodel import Field, SQLModel
from sqlalchemy import Column, Integer, Date, Text
from .base import Base


class Game(Base, table=True):
    """Game entity for poker sessions."""
    
    __tablename__ = "games"
    id: Optional[int] = Field(sa_column=Column(Integer, primary_key=True, autoincrement=True))
    created_at: date = Field(sa_column=Column(Date, default=date.today, nullable=False))
    description: Optional[str] = Field(default=None, sa_column=Column(Text))
    description: Optional[str] = Field(default=None, sa_column=Column(Text))
