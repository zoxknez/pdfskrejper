"""
Logging utilities.
"""

import logging
import sys
from pathlib import Path
from rich.logging import RichHandler
from rich.console import Console

console = Console()


def setup_logger(name: str = "pdf_scraper", level: str = "INFO") -> logging.Logger:
    """
    Postavlja logger sa Rich handler-om za lepo formatiranje.
    
    Args:
        name: Ime logger-a
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    
    Returns:
        Konfigurisan logger
    """
    # Kreiraj logs direktorijum
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Kreiraj logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    # Ukloni postojeće handlers
    logger.handlers.clear()
    
    # Rich handler za konzolu (lepo formatiran)
    rich_handler = RichHandler(
        console=console,
        rich_tracebacks=True,
        tracebacks_show_locals=True,
        markup=True
    )
    rich_handler.setLevel(logging.INFO)
    rich_formatter = logging.Formatter(
        "%(message)s",
        datefmt="[%X]"
    )
    rich_handler.setFormatter(rich_formatter)
    
    # File handler za detaljne logove
    file_handler = logging.FileHandler(
        log_dir / "scraper.log",
        encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(file_formatter)
    
    # Dodaj handlers
    logger.addHandler(rich_handler)
    logger.addHandler(file_handler)
    
    return logger


def get_logger(name: str = None) -> logging.Logger:
    """
    Vraća postojeći logger ili kreira novi.
    
    Args:
        name: Ime logger-a
    
    Returns:
        Logger instanca
    """
    if name is None:
        name = "pdf_scraper"
    
    logger = logging.getLogger(name)
    
    # Ako logger nema handlers, postavi ga
    if not logger.handlers:
        return setup_logger(name)
    
    return logger
