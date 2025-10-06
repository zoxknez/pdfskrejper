"""
Database konfiguracija i helper funkcije.
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db(app):
    """Inicijalizuje bazu podataka."""
    with app.app_context():
        db.create_all()
        print("✓ Database tables created")
