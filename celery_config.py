"""
Celery konfiguracija za PDF Scraper.
"""

import os

from celery import Celery
from celery.signals import task_failure, task_postrun, task_prerun
from dotenv import load_dotenv

load_dotenv()

# Redis URL
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Kreiraj Celery instancu
celery_app = Celery(
    "pdf_scraper", broker=REDIS_URL, backend=REDIS_URL, include=["web.celery_tasks"]
)

# Celery konfiguracija
celery_app.conf.update(
    # Task execution
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Europe/Belgrade",
    enable_utc=True,
    # Task routing
    task_routes={
        "web.celery_tasks.scrape_task": {"queue": "scraping"},
        "web.celery_tasks.download_task": {"queue": "downloads"},
    },
    # Task limits
    task_time_limit=3600,  # 1 sat
    task_soft_time_limit=3300,  # 55 minuta
    worker_max_tasks_per_child=50,
    # Results
    result_expires=3600,  # Rezultati ističu nakon 1 sata
    result_backend_transport_options={"master_name": "mymaster"},
    # Retry policy
    task_default_retry_delay=60,  # 1 minut
    task_max_retries=3,
    # Worker
    worker_prefetch_multiplier=4,
    worker_disable_rate_limits=False,
    # Beat (periodic tasks) - za budućnost
    beat_schedule={},
)


# Signali za logging
@task_prerun.connect
def task_prerun_handler(
    sender=None, task_id=None, task=None, args=None, kwargs=None, **extra
):
    """Handler koji se poziva pre pokretanja task-a."""
    print(f"Task {task.name} [{task_id}] starting...")


@task_postrun.connect
def task_postrun_handler(sender=None, task_id=None, task=None, retval=None, **extra):
    """Handler koji se poziva nakon završetka task-a."""
    print(f"Task {task.name} [{task_id}] completed successfully")


@task_failure.connect
def task_failure_handler(sender=None, task_id=None, exception=None, **extra):
    """Handler koji se poziva kada task padne."""
    print(f"Task [{task_id}] failed with exception: {exception}")


if __name__ == "__main__":
    celery_app.start()
