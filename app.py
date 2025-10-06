"""
PDF Scraper Web Application - Main Entry Point
Profesionalna web aplikacija sa login/register sistemom
"""

import os
import webbrowser
from datetime import datetime
from threading import Timer

from flask import Flask, flash, jsonify, redirect, render_template, request, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from werkzeug.security import check_password_hash, generate_password_hash

from config.settings import Settings
from config.sources import SourceType, get_sources_by_type
from utils.logger import get_logger
from web.database import db, init_db
from web.forms import LoginForm, RegisterForm, ScrapingForm
from web.models import DownloadedFile, ScrapingJob, User

logger = get_logger(__name__)

# Kreiraj Flask app
app = Flask(__name__)

# SECRET_KEY configuration - fail fast if not set in production
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    if os.getenv("FLASK_ENV") == "production":
        raise ValueError(
            "SECRET_KEY must be set in production environment! "
            "Set it in .env file or environment variables."
        )
    logger.warning("Using development SECRET_KEY - NOT FOR PRODUCTION!")
    SECRET_KEY = "dev-secret-key-only-for-development"

app.config["SECRET_KEY"] = SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pdf_scraper.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Inicijalizuj ekstenzije
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "Molimo prijavite se da biste pristupili ovoj stranici."

# Kreiraj direktorijume
Settings.create_directories()


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return db.session.get(User, int(user_id))


# ==================== AUTHENTICATION ROUTES ====================


@app.route("/")
def index():
    """Landing page - preusmerava na dashboard ili login."""
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    """Login stranica."""
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=form.remember.data)

            # Update last login
            user.last_login = datetime.utcnow()
            db.session.commit()

            flash("Uspešno ste se prijavili!", "success")
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("dashboard"))
        else:
            flash("Neispravna email adresa ili lozinka.", "danger")

    return render_template("login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Registracija korisnika."""
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    form = RegisterForm()
    if form.validate_on_submit():
        # Proveri da li korisnik već postoji
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash("Email adresa je već registrovana.", "warning")
            return redirect(url_for("register"))

        # Kreiraj novog korisnika
        try:
            hashed_password = generate_password_hash(form.password.data)
            new_user = User(
                username=form.username.data,
                email=form.email.data,
                password_hash=hashed_password,
            )

            db.session.add(new_user)
            db.session.commit()

            flash("Nalog je uspešno kreiran! Možete se prijaviti.", "success")
            return redirect(url_for("login"))
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating user: {e}")
            flash("Greška pri kreiranju naloga. Pokušajte ponovo.", "danger")
            return redirect(url_for("register"))

    return render_template("register.html", form=form)


@app.route("/logout")
@login_required
def logout():
    """Logout korisnika."""
    logout_user()
    flash("Uspešno ste se odjavili.", "info")
    return redirect(url_for("login"))


# ==================== MAIN APP ROUTES ====================


@app.route("/dashboard")
@login_required
def dashboard():
    """Glavni dashboard."""
    # Statistika korisnika
    total_jobs = ScrapingJob.query.filter_by(user_id=current_user.id).count()
    completed_jobs = ScrapingJob.query.filter_by(
        user_id=current_user.id, status="completed"
    ).count()
    total_files = DownloadedFile.query.filter_by(user_id=current_user.id).count()

    # Nedavni poslovi
    recent_jobs = (
        ScrapingJob.query.filter_by(user_id=current_user.id)
        .order_by(ScrapingJob.created_at.desc())
        .limit(10)
        .all()
    )

    return render_template(
        "dashboard.html",
        total_jobs=total_jobs,
        completed_jobs=completed_jobs,
        total_files=total_files,
        recent_jobs=recent_jobs,
    )


@app.route("/scrape", methods=["GET", "POST"])
@login_required
def scrape():
    """Stranica za pokretanje novog scraping job-a."""
    form = ScrapingForm()

    # Popuni choices za category i source
    form.category.choices = [(t.value, t.value.title()) for t in SourceType]

    if form.validate_on_submit():
        # Kreiraj novi scraping job
        job = ScrapingJob(
            user_id=current_user.id,
            category=form.category.data,
            source_name=form.source.data,
            search_query=form.query.data,
            max_results=form.max_results.data,
            status="pending",
        )

        try:
            db.session.add(job)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating job: {e}")
            flash("Greška pri kreiranju job-a.", "danger")
            return redirect(url_for("scrape"))

        # Pokreni scraping task preko Celery-ja (non-blocking)
        try:
            from web.celery_tasks import scrape_task

            task = scrape_task.delay(job.id)
            job.celery_task_id = task.id
            db.session.commit()

            flash(
                "Scraping je pokrenut u pozadini! Možete pratiti napredak.", "success"
            )
            logger.info(f"Scraping task started: job_id={job.id}, task_id={task.id}")
        except Exception as e:
            db.session.rollback()
            job.status = "failed"
            job.error_message = f"Greška pri pokretanju task-a: {str(e)}"
            try:
                db.session.commit()
            except Exception as commit_error:
                db.session.rollback()
                logger.error(f"Error committing failed status: {commit_error}")
            flash(f"Greška pri pokretanju scraping-a: {e}", "danger")

        return redirect(url_for("job_status", job_id=job.id))

    # Lista svih izvora po kategorijama
    sources_by_category = {}
    for source_type in SourceType:
        sources = get_sources_by_type(source_type)
        sources_by_category[source_type.value] = [
            {"name": s.name, "description": s.description} for s in sources
        ]

    return render_template(
        "scrape.html", form=form, sources_by_category=sources_by_category
    )


@app.route("/job/<int:job_id>")
@login_required
def job_status(job_id):
    """Status pojedinačnog scraping job-a."""
    job = ScrapingJob.query.get_or_404(job_id)

    # Proveri da li job pripada trenutnom korisniku
    if job.user_id != current_user.id:
        flash("Nemate pristup ovom job-u.", "danger")
        return redirect(url_for("dashboard"))

    # Preuzeti fajlovi za ovaj job
    files = DownloadedFile.query.filter_by(job_id=job_id).all()

    return render_template("job_status.html", job=job, files=files)


@app.route("/files")
@login_required
def files():
    """Lista svih preuzetih fajlova."""
    page = request.args.get("page", 1, type=int)
    category = request.args.get("category", None)

    query = DownloadedFile.query.filter_by(user_id=current_user.id)

    if category:
        query = query.filter_by(category=category)

    files_pagination = query.order_by(DownloadedFile.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )

    return render_template(
        "files.html",
        files=files_pagination.items,
        pagination=files_pagination,
        current_category=category,
    )


@app.route("/profile")
@login_required
def profile():
    """Korisnički profil."""
    # Statistika
    total_jobs = ScrapingJob.query.filter_by(user_id=current_user.id).count()
    completed_jobs = ScrapingJob.query.filter_by(
        user_id=current_user.id, status="completed"
    ).count()
    total_files = DownloadedFile.query.filter_by(user_id=current_user.id).count()

    # Kategorije
    category_stats = (
        db.session.query(
            ScrapingJob.category, db.func.count(ScrapingJob.id).label("count")
        )
        .filter_by(user_id=current_user.id)
        .group_by(ScrapingJob.category)
        .all()
    )

    # Total veličina fajlova
    total_size_result = (
        db.session.query(db.func.sum(DownloadedFile.file_size))
        .filter_by(user_id=current_user.id)
        .scalar()
    )
    total_size = round(total_size_result / (1024 * 1024), 2) if total_size_result else 0

    # Nedavni poslovi
    recent_jobs = (
        ScrapingJob.query.filter_by(user_id=current_user.id)
        .order_by(ScrapingJob.created_at.desc())
        .limit(10)
        .all()
    )

    stats = {
        "total_jobs": total_jobs,
        "completed_jobs": completed_jobs,
        "total_files": total_files,
    }

    return render_template(
        "profile.html",
        user=current_user,
        stats=stats,
        category_stats=category_stats,
        total_size=total_size,
        recent_jobs=recent_jobs,
    )


@app.route("/about")
def about():
    """O programu stranica."""
    return render_template("about.html")


# ==================== API ROUTES ====================


@app.route("/api/sources/<category>")
@login_required
def api_get_sources(category):
    """API endpoint za dobijanje izvora po kategoriji."""
    try:
        source_type = SourceType(category)
        sources = get_sources_by_type(source_type)
        return jsonify(
            [
                {"name": s.name, "description": s.description, "url": s.url}
                for s in sources
            ]
        )
    except ValueError:
        return jsonify({"error": "Invalid category"}), 400


@app.route("/api/job/<int:job_id>/status")
@login_required
def api_job_status(job_id):
    """API endpoint za status job-a (za real-time updates)."""
    job = ScrapingJob.query.get_or_404(job_id)

    if job.user_id != current_user.id:
        return jsonify({"error": "Unauthorized"}), 403

    response = {
        "id": job.id,
        "status": job.status,
        "progress": job.progress,
        "total_found": job.total_found,
        "total_downloaded": job.total_downloaded,
        "total_failed": job.total_failed,
        "error_message": job.error_message,
    }

    # Ako postoji Celery task ID, dodaj info o task-u
    if job.celery_task_id:
        try:
            from celery.result import AsyncResult

            task_result = AsyncResult(job.celery_task_id)
            response["celery_status"] = task_result.status
            response["celery_ready"] = task_result.ready()
        except Exception as e:
            logger.debug(f"Celery status unavailable for job {job_id}: {e}")
            # Celery nije dostupan, ignoriši

    return jsonify(response)


@app.route("/api/stats")
@login_required
def api_stats():
    """API endpoint za statistiku korisnika."""
    total_jobs = ScrapingJob.query.filter_by(user_id=current_user.id).count()
    total_files = DownloadedFile.query.filter_by(user_id=current_user.id).count()

    # Statistika po kategorijama
    categories_stats = (
        db.session.query(DownloadedFile.category, db.func.count(DownloadedFile.id))
        .filter_by(user_id=current_user.id)
        .group_by(DownloadedFile.category)
        .all()
    )

    return jsonify(
        {
            "total_jobs": total_jobs,
            "total_files": total_files,
            "categories": {cat: count for cat, count in categories_stats},
        }
    )


# ==================== ERROR HANDLERS ====================


@app.errorhandler(404)
def not_found_error(error):
    """404 stranica."""
    return render_template("errors/404.html"), 404


@app.errorhandler(500)
def internal_error(error):
    """500 stranica."""
    db.session.rollback()
    return render_template("errors/500.html"), 500


# ==================== CLI COMMANDS ====================


@app.cli.command()
def init_db_cmd():
    """Initialize the database."""
    init_db(app)
    print("Database initialized!")


@app.cli.command()
def create_admin_user():
    """Create admin user."""
    admin = User(
        username="admin",
        email="admin@pdfscraper.com",
        password_hash=generate_password_hash("admin123"),
        is_admin=True,
    )
    db.session.add(admin)
    db.session.commit()
    print("Admin user created: admin@pdfscraper.com / admin123")


# ==================== STATIC ROUTES FOR LOCALIZATION ====================


@app.route("/static/locales/<lang>.json")
def serve_locale(lang):
    """Serve language JSON files."""
    if lang not in ["sr", "en"]:
        return jsonify({"error": "Language not supported"}), 404

    import json

    locale_path = os.path.join(app.static_folder, "locales", f"{lang}.json")

    if not os.path.exists(locale_path):
        return jsonify({"error": "Locale file not found"}), 404

    with open(locale_path, "r", encoding="utf-8") as f:
        return jsonify(json.load(f))


@app.route("/test-theme")
def test_theme():
    """Test page for theme and language switching."""
    return render_template("test_theme.html")


# ==================== MAIN ====================


def open_browser():
    """Otvara browser nakon što server startuje."""
    webbrowser.open_new("http://127.0.0.1:5000/")


if __name__ == "__main__":
    # Kreiraj tabele ako ne postoje
    with app.app_context():
        init_db(app)

    # Otvori browser nakon 1.5 sekundi
    Timer(1.5, open_browser).start()

    # Pokreni Flask development server
    print("=" * 60)
    print("🚀 PDF SCRAPER WEB APPLICATION")
    print("=" * 60)
    print("📍 URL: http://127.0.0.1:5000")
    print("🌐 Browser će se automatski otvoriti...")
    print("⚠️  Za zaustavljanje: CTRL+C")
    print("=" * 60)

    app.run(debug=True, use_reloader=True)
