"""
Web aplikacija moduli.
"""

from .database import db
from .models import DownloadedFile, ScrapingJob, User

__all__ = ["db", "User", "ScrapingJob", "DownloadedFile"]
