"""
Scraper moduli za različite tipove dokumenata.
"""

from .base_scraper import BaseScraper
from .books_scraper import BooksScraper
from .research_scraper import ResearchScraper
from .magazine_scraper import MagazineScraper

__all__ = [
    'BaseScraper',
    'BooksScraper',
    'ResearchScraper',
    'MagazineScraper',
]
