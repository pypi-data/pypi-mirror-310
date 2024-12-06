"""Logging library to conform to Louder's logging standards."""

from __future__ import annotations

__all__ = ("setup", "Entry")


from ldr.logging.models import Entry
from ldr.logging.setup import setup
