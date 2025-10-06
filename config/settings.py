"""
Globalne postavke aplikacije.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# Učitaj .env fajl
load_dotenv()


class Settings:
    """Globalne postavke aplikacije."""

    # Osnovni direktorijumi
    BASE_DIR = Path(__file__).parent.parent
    STORAGE_DIR = Path(os.getenv("CRAWLEE_STORAGE_DIR", "./storage"))
    OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", "./downloaded_pdfs"))

    # Crawlee konfiguracija
    LOG_LEVEL = os.getenv("CRAWLEE_LOG_LEVEL", "INFO")
    DEFAULT_DATASET_ID = os.getenv("CRAWLEE_DEFAULT_DATASET_ID", "default")

    # Download konfiguracija
    MAX_CONCURRENT_DOWNLOADS = int(os.getenv("MAX_CONCURRENT_DOWNLOADS", "3"))
    DOWNLOAD_TIMEOUT = int(os.getenv("DOWNLOAD_TIMEOUT", "300"))
    USER_AGENT = os.getenv(
        "USER_AGENT", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    )

    # Request konfiguracija
    MAX_REQUEST_RETRIES = 3
    REQUEST_TIMEOUT = 30

    # Crawlee browser options
    HEADLESS = True
    BROWSER_TYPE = "chromium"  # chromium, firefox, webkit

    # Limits
    MAX_REQUESTS_PER_CRAWL = 100
    MAX_CRAWL_DEPTH = 3

    @classmethod
    def create_directories(cls):
        """Kreira potrebne direktorijume."""
        cls.STORAGE_DIR.mkdir(parents=True, exist_ok=True)
        cls.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        # Kreiraj poddirektorijume za različite kategorije
        categories = ["books", "research", "magazines", "documents", "other"]
        for category in categories:
            (cls.OUTPUT_DIR / category).mkdir(parents=True, exist_ok=True)

    @classmethod
    def get_output_dir(cls, category: str) -> Path:
        """Vraća output direktorijum za specifičnu kategoriju."""
        return cls.OUTPUT_DIR / category
