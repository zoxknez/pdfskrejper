"""
Web aplikacija moduli.
"""

from .database import db
from .models import User, ScrapingJob, DownloadedFile

__all__ = ['db', 'User', 'ScrapingJob', 'DownloadedFile']
