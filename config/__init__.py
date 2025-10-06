"""
Konfiguracioni modul za PDF Scraper aplikaciju.
"""

from .settings import Settings
from .sources import SOURCES, SourceType

__all__ = ['Settings', 'SOURCES', 'SourceType']
