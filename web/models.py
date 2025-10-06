"""
Database modeli za web aplikaciju.
"""

from datetime import datetime
from flask_login import UserMixin
from .database import db


class User(UserMixin, db.Model):
    """Korisnički model."""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relationships
    scraping_jobs = db.relationship('ScrapingJob', backref='user', lazy=True)
    downloaded_files = db.relationship('DownloadedFile', backref='user', lazy=True)
    
    def __repr__(self):
        return f'<User {self.username}>'


class ScrapingJob(db.Model):
    """Model za scraping poslove."""
    __tablename__ = 'scraping_jobs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Job configuration
    category = db.Column(db.String(50), nullable=False)
    source_name = db.Column(db.String(100))
    search_query = db.Column(db.String(200))
    max_results = db.Column(db.Integer, default=50)
    
    # Job status
    status = db.Column(
        db.String(20),
        default='pending'
    )  # pending, running, completed, failed
    progress = db.Column(db.Integer, default=0)
    
    # Results
    total_found = db.Column(db.Integer, default=0)
    total_downloaded = db.Column(db.Integer, default=0)
    total_failed = db.Column(db.Integer, default=0)
    
    # Metadata
    error_message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    
    # Relationships
    downloaded_files = db.relationship(
        'DownloadedFile',
        backref='job',
        lazy=True
    )
    
    def __repr__(self):
        return f'<ScrapingJob {self.id} - {self.status}>'
    
    @property
    def duration(self):
        """Trajanje job-a u sekundama."""
        if self.started_at and self.completed_at:
            return (self.completed_at - self.started_at).total_seconds()
        return None
    
    @property
    def success_rate(self):
        """Procenat uspešnosti."""
        total = self.total_downloaded + self.total_failed
        if total > 0:
            return (self.total_downloaded / total) * 100
        return 0


class DownloadedFile(db.Model):
    """Model za preuzete fajlove."""
    __tablename__ = 'downloaded_files'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('scraping_jobs.id'))
    
    # File info
    filename = db.Column(db.String(255), nullable=False)
    filepath = db.Column(db.String(500), nullable=False)
    category = db.Column(db.String(50))
    source_url = db.Column(db.String(500))
    
    # Metadata
    title = db.Column(db.String(500))
    file_size = db.Column(db.Integer)  # u bajtovima
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<DownloadedFile {self.filename}>'
    
    @property
    def file_size_mb(self):
        """Veličina fajla u MB."""
        if self.file_size:
            return round(self.file_size / (1024 * 1024), 2)
        return 0
