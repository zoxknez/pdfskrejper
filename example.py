"""
Primer skripte za korišćenje PDF Scraper-a.
"""

import asyncio
from config.sources import SourceType, get_sources_by_type
from scrapers import ResearchScraper
from config.settings import Settings

async def main():
    """Primer upotrebe."""
    
    # Kreiraj direktorijume
    Settings.create_directories()
    
    # Uzmi arXiv izvor
    sources = get_sources_by_type(SourceType.RESEARCH)
    arxiv_source = next((s for s in sources if s.name == "arXiv"), None)
    
    if not arxiv_source:
        print("arXiv izvor nije pronađen!")
        return
    
    # Kreiraj scraper
    scraper = ResearchScraper(
        source=arxiv_source,
        max_results=10  # Samo 10 rezultata za test
    )
    
    # Pokreni scraping
    print("Započinjem scraping arXiv radova o machine learning...")
    stats = await scraper.scrape(query="machine learning")
    
    # Prikaži rezultate
    print("\n" + "="*60)
    print("REZULTATI:")
    print("="*60)
    print(f"Pronađeno PDF-ova: {stats['total_urls_found']}")
    print(f"Uspešno preuzeto: {stats['total_downloaded']}")
    print(f"Neuspešno: {stats['total_failed']}")
    print(f"Uspešnost: {stats['success_rate']:.1f}%")
    print("="*60)
    
    # Zatvori resurse
    await scraper.close()

if __name__ == '__main__':
    asyncio.run(main())
