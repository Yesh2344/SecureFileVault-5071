"""
Centralised logging configuration.
"""

import logging
import sys
from pathlib import Path
from typing import Optional

def setup_logger(name: str = "SecureFileVault", level: Optional[str] = None) -> logging.Logger:
    """
    Configure and return a logger.

    Args:
        name: Logger name.
        level: Logging level string (e.g., "DEBUG"). If ``None``,
            the level is read from the configuration file.

    Returns:
        Configured ``logging.Logger`` instance.
    """
    logger = logging.getLogger(name)
    if logger.handlers:
        # Logger already configured
        return logger

    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    formatter = logging.Formatter(log_format)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    logger.setLevel(level or logging.INFO)
    logger.propagate = False
    return logger