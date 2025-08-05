#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
from zoneinfo import ZoneInfo

# Project timezone
SAO_PAULO_TZ = ZoneInfo("America/Sao_Paulo")


def now() -> datetime:
    """Get current datetime in São Paulo timezone."""
    return datetime.now(SAO_PAULO_TZ)


def utc_to_sao_paulo(dt: datetime) -> datetime:
    """Convert UTC datetime to São Paulo timezone."""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=ZoneInfo("UTC"))
    return dt.astimezone(SAO_PAULO_TZ)


def sao_paulo_to_utc(dt: datetime) -> datetime:
    """Convert São Paulo datetime to UTC."""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=SAO_PAULO_TZ)
    return dt.astimezone(ZoneInfo("UTC"))
