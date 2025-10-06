"""
Database konfiguracija i helper funkcije.
"""

import logging

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
logger = logging.getLogger(__name__)


def init_db(app):
    """Inicijalizuje bazu podataka."""
    with app.app_context():
        db.create_all()
        logger.info("Database tables created successfully")
