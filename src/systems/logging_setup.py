"""Logging setup for the application."""

import logging
from pathlib import Path
import os
from src.constants import LOG_FILE, APPDATA_DIR, MAX_LOG_SIZE


def setup_logging() -> logging.Logger:
    """Configure and return the application logger.

    Creates the application data directory if it doesn't exist, manages log file
    size by truncating when it exceeds MAX_LOG_SIZE, and configures a file handler
    with timestamp formatting. The log level can be controlled via the SPS_LOG_LEVEL
    environment variable.

    Returns:
        logging.Logger: The configured application logger instance.
    """
    APPDATA_DIR.mkdir(parents=True, exist_ok=True)
    
    # Check log file size and truncate if needed
    if LOG_FILE.exists() and LOG_FILE.stat().st_size > MAX_LOG_SIZE:
        LOG_FILE.unlink()
    
    # Get log level from environment
    log_level_str = os.environ.get("SPS_LOG_LEVEL", "INFO").upper()
    log_level = getattr(logging, log_level_str, logging.INFO)
    
    # Configure logger
    logger = logging.getLogger("SerpentsPerSecond")
    logger.setLevel(log_level)
    
    # Remove existing handlers
    logger.handlers.clear()
    
    # File handler
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setLevel(log_level)
    
    # Formatter
    formatter = logging.Formatter(
        "%(asctime)s.%(msecs)03d | %(levelname)s | %(module)s:%(funcName)s:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger


def get_logger() -> logging.Logger:
    """Get the application logger.

    Retrieves the existing logger instance by name. This should be called after
    setup_logging() has been invoked to ensure the logger is properly configured.

    Returns:
        logging.Logger: The application logger instance.
    """
    return logging.getLogger("SerpentsPerSecond")
