"""
Database migration helper script.
Initialize Flask-Migrate for the project.
"""

from flask_migrate import Migrate
from app import app
from web.database import db

# Initialize Flask-Migrate
migrate = Migrate(app, db)

if __name__ == "__main__":
    print("Flask-Migrate initialized!")
    print("Run the following commands:")
    print("  flask --app migrate_db db init")
    print("  flask --app migrate_db db migrate -m 'Initial migration'")
    print("  flask --app migrate_db db upgrade")
