"""
Background tasks za scraping.
"""

import asyncio
from datetime import datetime
from pathlib import Path

from config.sources import SourceType, get_source_by_name
from scrapers import BooksScraper, MagazineScraper, ResearchScraper
from web.database import db
from web.models import DownloadedFile, ScrapingJob


async def run_scraping_task(job_id: int):
    """
    Pokreće scraping task za dati job ID.

    Args:
        job_id: ID scraping job-a
    """
    from app import app

    with app.app_context():
        # Učitaj job
        job = ScrapingJob.query.get(job_id)
        if not job:
            return

        try:
            # Update status
            job.status = "running"
            job.started_at = datetime.utcnow()
            db.session.commit()

            # Pripremi scraper
            category = SourceType(job.category)
            source = get_source_by_name(job.source_name)

            if not source:
                raise ValueError(f"Source {job.source_name} not found")

            # Izaberi scraper klasu
            scraper_map = {
                SourceType.BOOKS: BooksScraper,
                SourceType.RESEARCH: ResearchScraper,
                SourceType.MAGAZINES: MagazineScraper,
                SourceType.DOCUMENTS: BooksScraper,
            }

            scraper_class = scraper_map.get(category, BooksScraper)
            scraper = scraper_class(source=source, max_results=job.max_results)

            # Pokreni scraping
            stats = await scraper.scrape(query=job.search_query or "")

            # Update job sa rezultatima
            job.status = "completed"
            job.completed_at = datetime.utcnow()
            job.total_found = stats.get("total_urls_found", 0)
            job.total_downloaded = stats.get("total_downloaded", 0)
            job.total_failed = stats.get("total_failed", 0)
            job.progress = 100

            # Sačuvaj informacije o preuzetim fajlovima
            for filepath_str in stats.get("downloaded_files", []):
                filepath = Path(filepath_str)

                downloaded_file = DownloadedFile(
                    user_id=job.user_id,
                    job_id=job.id,
                    filename=filepath.name,
                    filepath=str(filepath),
                    category=job.category,
                    file_size=filepath.stat().st_size if filepath.exists() else 0,
                )

                db.session.add(downloaded_file)

            db.session.commit()

        except Exception as e:
            # Update job sa greškom
            job.status = "failed"
            job.error_message = str(e)
            job.completed_at = datetime.utcnow()
            db.session.commit()
            raise
