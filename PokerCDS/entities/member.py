#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel
from sqlalchemy import Column, Integer, DateTime
from pydantic import field_validator
from .base import Base
from ..utils.timezone import now
from ..utils.password import hash_password


class Member(Base, table=True):
    """Member entity for poker group registration."""
    
    __tablename__ = "members"
    id: Optional[int] = Field(sa_column=Column(Integer, primary_key=True, autoincrement=True))
    cpf: str = Field(max_length=11, unique=True, index=True)
    name: str = Field(max_length=64)
    nickname: str = Field(max_length=48)
    email: str = Field(max_length=255)
    pix_key: str = Field(max_length=128)
    phone: Optional[str] = Field(default=None, max_length=20)
    password: Optional[str] = Field(default=None, max_length=128)  # bcrypt hashes are 60 chars
    is_admin: Optional[bool] = Field(default=False)
    is_enabled: Optional[bool] = Field(default=True)
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), default=now, nullable=False))
    updated_at: Optional[datetime] = Field(sa_column=Column(DateTime(timezone=True), default=None))

    @field_validator('cpf')
    @classmethod
    def validate_cpf(cls, v: str) -> str:
        """Validate and clean CPF format."""
        # Remove all non-digit characters
        cpf = ''.join(filter(str.isdigit, v))
        
        # Pad with zeros if less than 11 digits
        cpf = cpf.zfill(11)
        
        # Check if CPF has more than 11 digits after padding
        if len(cpf) > 11:
            raise ValueError('CPF deve ter no máximo 11 dígitos')
        return cpf

    @field_validator('password')
    @classmethod
    def hash_password_field(cls, v: Optional[str]) -> Optional[str]:
        """Hash password if provided."""
        if v is None:
            return v
        return hash_password(v)
