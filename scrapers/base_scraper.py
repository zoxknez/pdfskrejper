"""
Bazna klasa za sve scrapere.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Optional

from crawlee.crawlers import PlaywrightCrawler, PlaywrightCrawlingContext

from config.settings import Settings
from config.sources import Source
from utils.downloader import PDFDownloader
from utils.logger import get_logger

logger = get_logger(__name__)


class BaseScraper(ABC):
    """Bazna klasa za sve PDF scrapere."""

    def __init__(
        self, source: Source, max_results: int = 50, output_dir: Optional[Path] = None
    ):
        """
        Inicijalizuje scraper.

        Args:
            source: Izvor za scraping
            max_results: Maksimalan broj rezultata
            output_dir: Output direktorijum
        """
        self.source = source
        self.max_results = max_results
        self.output_dir = output_dir or Settings.get_output_dir(
            source.source_type.value
        )
        self.downloader = PDFDownloader(output_dir=self.output_dir)
        self.pdf_urls: List[str] = []
        self.metadata: List[Dict] = []

    @abstractmethod
    async def extract_pdf_urls(self, context: PlaywrightCrawlingContext):
        """
        Izvlači PDF URL-ove sa stranice.
        Mora biti implementiran u child klasama.

        Args:
            context: Crawlee context
        """
        pass

    async def scrape(self, query: str = "") -> Dict:
        """
        Glavni scraping metod.

        Args:
            query: Search query (opcionalno)

        Returns:
            Statistika scraping-a
        """
        logger.info(
            f"Započinjem scraping: {self.source.name} "
            f"[{self.source.source_type.value}]"
        )

        if query:
            logger.info(f"Query: {query}")

        # Kreiraj crawler
        crawler = PlaywrightCrawler(
            max_requests_per_crawl=self.max_results,
            headless=Settings.HEADLESS,
            browser_type=Settings.BROWSER_TYPE,
        )

        # Postavi request handler
        @crawler.router.default_handler
        async def request_handler(context: PlaywrightCrawlingContext) -> None:
            await self.extract_pdf_urls(context)

        # Start URL
        start_url = self._build_url(query)
        logger.info(f"Start URL: {start_url}")

        # Pokreni crawler
        await crawler.run([start_url])

        # Preuzmi PDFove
        logger.info(f"Pronađeno {len(self.pdf_urls)} PDF URL-ova")

        if self.pdf_urls:
            logger.info("Započinjem preuzimanje...")
            await self.downloader.download_multiple(
                self.pdf_urls, category=self.source.source_type.value
            )

        # Statistika
        stats = self.downloader.get_statistics()
        stats["source"] = self.source.name
        stats["category"] = self.source.source_type.value
        stats["total_urls_found"] = len(self.pdf_urls)

        self._print_summary(stats)

        return stats

    def _build_url(self, query: str = "") -> str:
        """Kreira URL sa query parametrom."""
        if query and "search_url" in self.source.selectors:
            return self.source.selectors["search_url"].format(query=query)
        return self.source.url

    def _print_summary(self, stats: Dict):
        """Ispisuje sažetak rezultata."""
        logger.info("=" * 60)
        logger.info("📊 REZULTATI SCRAPING-A")
        logger.info("=" * 60)
        logger.info(f"Izvor: {stats['source']}")
        logger.info(f"Kategorija: {stats['category']}")
        logger.info(f"Pronađeno URL-ova: {stats['total_urls_found']}")
        logger.info(f"Uspešno preuzeto: {stats['total_downloaded']}")
        logger.info(f"Neuspešno: {stats['total_failed']}")
        logger.info(f"Uspešnost: {stats['success_rate']:.1f}%")
        logger.info("=" * 60)

    async def close(self):
        """Zatvara resurse."""
        # Cleanup ako je potrebno
        pass
