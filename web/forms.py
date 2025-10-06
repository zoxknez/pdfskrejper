"""
WTForms za web aplikaciju.
"""

from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    IntegerField,
    PasswordField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    NumberRange,
    ValidationError,
)

from .models import User


class LoginForm(FlaskForm):
    """Login forma."""

    email = StringField(
        "Email",
        validators=[DataRequired(), Email()],
        render_kw={"placeholder": "vasa@email.com"},
    )
    password = PasswordField(
        "Lozinka",
        validators=[DataRequired()],
        render_kw={"placeholder": "Unesite lozinku"},
    )
    remember = BooleanField("Zapamti me")
    submit = SubmitField("Prijavi se")


class RegisterForm(FlaskForm):
    """Registraciona forma."""

    username = StringField(
        "Korisničko ime",
        validators=[
            DataRequired(),
            Length(min=3, max=80, message="Mora biti između 3 i 80 karaktera"),
        ],
        render_kw={"placeholder": "korisnik123"},
    )
    email = StringField(
        "Email",
        validators=[DataRequired(), Email()],
        render_kw={"placeholder": "vasa@email.com"},
    )
    password = PasswordField(
        "Lozinka",
        validators=[
            DataRequired(),
            Length(min=6, message="Lozinka mora imati najmanje 6 karaktera"),
        ],
        render_kw={"placeholder": "Unesite lozinku"},
    )
    confirm_password = PasswordField(
        "Potvrdite lozinku",
        validators=[
            DataRequired(),
            EqualTo("password", message="Lozinke se ne poklapaju"),
        ],
        render_kw={"placeholder": "Ponovite lozinku"},
    )
    submit = SubmitField("Registruj se")

    def validate_username(self, username):
        """Proveri da li korisničko ime već postoji."""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Korisničko ime je već zauzeto.")

    def validate_email(self, email):
        """Proveri da li email već postoji."""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email adresa je već registrovana.")


class ScrapingForm(FlaskForm):
    """Forma za pokretanje scraping job-a."""

    category = SelectField(
        "Kategorija", validators=[DataRequired()], choices=[]  # Popunjava se dinamički
    )
    source = StringField(
        "Izvor",
        validators=[DataRequired()],
        render_kw={"placeholder": "Izaberite izvor..."},
    )
    query = StringField(
        "Pretraga (opcionalno)", render_kw={"placeholder": "npr. machine learning"}
    )
    max_results = IntegerField(
        "Maksimalan broj rezultata",
        validators=[
            DataRequired(),
            NumberRange(min=1, max=500, message="Mora biti između 1 i 500"),
        ],
        default=50,
    )
    submit = SubmitField("Pokreni Scraping")
