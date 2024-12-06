"""Configure the python standard logger for structured logging."""

from __future__ import annotations

import logging

from google.cloud.logging.handlers import StructuredLogHandler
from google.cloud.logging_v2 import handlers


def setup(level: int = logging.NOTSET) -> None:
    """Configure the python standard logger for structured logging."""
    handler = StructuredLogHandler()
    handlers.setup_logging(handler, log_level=level)
