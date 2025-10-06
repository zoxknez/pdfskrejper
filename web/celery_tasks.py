"""
Celery tasks za scraping operacije.
"""

import asyncio
from datetime import datetime
from pathlib import Path

from celery import Task
from celery.utils.log import get_task_logger

from celery_config import celery_app
from config.sources import SourceType, get_source_by_name
from scrapers import BooksScraper, MagazineScraper, ResearchScraper

logger = get_task_logger(__name__)


class DatabaseTask(Task):
    """Bazna klasa za task-ove koji koriste Flask app context."""

    _app = None

    @property
    def app_context(self):
        """Lazy-loaded Flask app context."""
        if self._app is None:
            from app import app as flask_app

            self._app = flask_app
        return self._app.app_context()


@celery_app.task(bind=True, base=DatabaseTask, name="web.celery_tasks.scrape_task")
def scrape_task(self, job_id: int):
    """
    Celery task za scraping.

    Args:
        job_id: ID scraping job-a

    Returns:
        dict: Statistika scraping-a
    """
    logger.info(f"Starting scraping task for job_id={job_id}")

    with self.app_context():
        from web.database import db
        from web.models import DownloadedFile, ScrapingJob

        # Učitaj job
        job = db.session.get(ScrapingJob, job_id)
        if not job:
            logger.error(f"Job {job_id} not found")
            return {"error": "Job not found"}

        try:
            # Update status
            job.status = "running"
            job.started_at = datetime.utcnow()
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise

            logger.info(f"Job {job_id}: Status updated to 'running'")

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

            logger.info(f"Job {job_id}: Starting scraper for {source.name}")

            # Pokreni scraping (asyncio)
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                stats = loop.run_until_complete(
                    scraper.scrape(query=job.search_query or "")
                )
            finally:
                loop.close()

            logger.info(f"Job {job_id}: Scraping completed. Stats: {stats}")

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

            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                logger.error(f"Job {job_id}: Error saving files: {e}")
                raise

            logger.info(f"Job {job_id}: Completed successfully")

            return {"status": "success", "job_id": job_id, "stats": stats}

        except Exception as e:
            logger.exception(f"Job {job_id}: Failed with error: {e}")

            # Update job sa greškom
            db.session.rollback()
            job.status = "failed"
            job.error_message = str(e)
            job.completed_at = datetime.utcnow()
            try:
                db.session.commit()
            except Exception as commit_error:
                db.session.rollback()
                logger.error(f"Job {job_id}: Error saving failure: {commit_error}")

            # Retry task
            raise self.retry(exc=e, countdown=60, max_retries=2)


@celery_app.task(name="web.celery_tasks.update_job_progress")
def update_job_progress(job_id: int, progress: int, status: str = None):
    """
    Task za ažuriranje progresa job-a.

    Args:
        job_id: ID job-a
        progress: Progress percentage (0-100)
        status: Optional status update
    """
    from app import app as flask_app

    with flask_app.app_context():
        from web.database import db
        from web.models import ScrapingJob

        job = db.session.get(ScrapingJob, job_id)
        if job:
            job.progress = progress
            if status:
                job.status = status
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                logger.error(f"Error updating progress for job {job_id}: {e}")
            logger.info(f"Job {job_id}: Progress updated to {progress}%")


@celery_app.task(name="web.celery_tasks.cleanup_old_jobs")
def cleanup_old_jobs(days: int = 30):
    """
    Periodic task za čišćenje starih job-ova.

    Args:
        days: Broj dana posle kojih se job-ovi brišu
    """
    from datetime import timedelta

    from app import app as flask_app

    with flask_app.app_context():
        from web.database import db
        from web.models import ScrapingJob

        cutoff_date = datetime.utcnow() - timedelta(days=days)
        old_jobs = ScrapingJob.query.filter(
            ScrapingJob.created_at < cutoff_date,
            ScrapingJob.status.in_(["completed", "failed"]),
        ).all()

        for job in old_jobs:
            db.session.delete(job)

        db.session.commit()
        logger.info(f"Cleaned up {len(old_jobs)} old jobs")
