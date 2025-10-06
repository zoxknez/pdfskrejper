"""
Scraper moduli za različite tipove dokumenata.
"""

from .base_scraper import BaseScraper
from .books_scraper import BooksScraper
from .magazine_scraper import MagazineScraper
from .research_scraper import ResearchScraper

__all__ = [
    "BaseScraper",
    "BooksScraper",
    "ResearchScraper",
    "MagazineScraper",
]
