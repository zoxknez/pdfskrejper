"""
Glavni ulazni fajl za PDF Scraper aplikaciju.
"""

import argparse
import asyncio
import sys
from pathlib import Path

from config.settings import Settings
from config.sources import Source, SourceType, get_source_by_name
from scrapers import BooksScraper, MagazineScraper, ResearchScraper
from ui.menu import InteractiveMenu
from utils.logger import setup_logger

# Setup logger
logger = setup_logger("pdf_scraper", level="INFO")


def parse_arguments():
    """Parsira command line argumente."""
    parser = argparse.ArgumentParser(
        description="PDF Scraper - Automatsko preuzimanje PDF dokumenata"
    )

    parser.add_argument(
        "--category",
        choices=["books", "research", "magazines", "documents"],
        help="Kategorija dokumenata",
    )

    parser.add_argument(
        "--source", type=str, help='Ime izvora (npr. "arxiv", "gutenberg")'
    )

    parser.add_argument("--query", type=str, default="", help="Search query")

    parser.add_argument(
        "--limit", type=int, default=50, help="Maksimalan broj rezultata (default: 50)"
    )

    parser.add_argument(
        "--output", type=Path, help="Output direktorijum za preuzete fajlove"
    )

    parser.add_argument("--url", type=str, help="Custom URL za scraping")

    parser.add_argument(
        "--interactive", action="store_true", help="Pokreni interaktivni mod"
    )

    return parser.parse_args()


def get_scraper_for_category(category: SourceType, source: Source, **kwargs):
    """Vraća odgovarajući scraper za kategoriju."""
    scraper_map = {
        SourceType.BOOKS: BooksScraper,
        SourceType.RESEARCH: ResearchScraper,
        SourceType.MAGAZINES: MagazineScraper,
        SourceType.DOCUMENTS: BooksScraper,  # Generički
    }

    scraper_class = scraper_map.get(category, BooksScraper)
    return scraper_class(source=source, **kwargs)


async def run_scraper(config: dict):
    """Pokreće scraper sa datom konfiguracijom."""
    try:
        # Kreiraj direktorijume
        Settings.create_directories()

        # Pripremi scraper
        category = config["category"]
        source = config["source"]
        query = config.get("query", "")
        max_results = config.get("max_results", 50)
        output_dir = config.get("output_dir", None)

        # Custom URL logika
        if config.get("custom_url"):
            source = Source(
                name="Custom",
                url=config["custom_url"],
                source_type=SourceType.DOCUMENTS,
                description="Custom URL",
            )

        logger.info(f"Pokrećem scraper za: {category.value}")

        # Kreiraj scraper
        scraper = get_scraper_for_category(
            category=category,
            source=source,
            max_results=max_results,
            output_dir=output_dir,
        )

        # Pokreni scraping
        stats = await scraper.scrape(query=query)

        # Zatvori resurse
        await scraper.close()

        return stats

    except Exception as e:
        logger.error(f"Greška pri pokretanju scraper-a: {e}", exc_info=True)
        return None


async def interactive_mode():
    """Pokreće interaktivni mod."""
    menu = InteractiveMenu()
    config = menu.run()

    if not config:
        logger.info("Otkazano od strane korisnika.")
        return

    # Pokreni scraper
    stats = await run_scraper(config)

    # Prikaži rezultate
    if stats:
        InteractiveMenu.show_results(stats)


async def command_line_mode(args):
    """Pokreće command line mod."""
    # Validacija argumenata
    if not args.category:
        logger.error("Morate specifikovati --category")
        sys.exit(1)

    # Konvertuj category string u SourceType
    category = SourceType(args.category)

    # Pronađi izvor
    source = None
    if args.source:
        source = get_source_by_name(args.source)
        if not source:
            logger.error(f"Izvor '{args.source}' nije pronađen")
            sys.exit(1)
    else:
        # Uzmi prvi izvor za kategoriju
        from config.sources import get_sources_by_type

        sources = get_sources_by_type(category)
        if sources:
            source = sources[0]
        else:
            logger.error(f"Nema dostupnih izvora za kategoriju {category.value}")
            sys.exit(1)

    # Pripremi config
    config = {
        "category": category,
        "source": source,
        "query": args.query,
        "max_results": args.limit,
        "output_dir": args.output,
        "custom_url": args.url,
    }

    # Pokreni scraper
    stats = await run_scraper(config)

    # Prikaži rezultate
    if stats:
        logger.info(f"\nRezultati: {stats}")


async def main():
    """Glavna funkcija."""
    args = parse_arguments()

    # Odluči koji mod koristiti
    if args.interactive or (not args.category and not args.url):
        # Interaktivni mod
        await interactive_mode()
    else:
        # Command line mod
        await command_line_mode(args)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("\nPrekinuto od strane korisnika.")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Neočekivana greška: {e}", exc_info=True)
        sys.exit(1)
