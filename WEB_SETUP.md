# Web Application Setup & Testing Guide

## 🎉 Cestitamo! Web aplikacija je uspešno kreirana!

## 📋 Status

✅ Flask server pokrenut na http://127.0.0.1:5000
✅ Baza podataka inicijalizovana
✅ Browser automatski otvoren
✅ Sve template-e kreirane
✅ Static fajlovi (CSS/JS) kreirani

## 🚀 Prvo pokretanje

Aplikacija je već pokrenuta! Možete pristupiti na:
- **URL**: http://127.0.0.1:5000
- **Browser**: Automatski se otvara

## 👤 Kreiranje prvog korisnika

Opcija 1 - Kroz register stranicu (PREPORUČENO):
1. Idite na http://127.0.0.1:5000/register
2. Popunite formu:
   - Username: testuser
   - Email: test@example.com
   - Password: test123
   - Confirm Password: test123
3. Kliknite "Registruj se"
4. Prijavite se sa kreiranim nalogom

Opcija 2 - Kreira admin korisnika kroz CLI:
```powershell
flask create-admin-user
```
Kredencijali: admin@pdfscraper.com / admin123

## 📖 Korišćenje Aplikacije

### 1. Dashboard
- Pregled statistike (ukupno job-ova, završenih job-ova, fajlova)
- Lista nedavnih scraping job-ova
- Brzi pristup funkcijama

### 2. Novi Scraping
- Kliknite "Novi Scraping" u navbar-u
- Izaberite kategoriju (Knjige, Naučni Radovi, Časopisi)
- Odaberite izvor (arXiv, PubMed, Gutenberg, itd.)
- Unesite opcionalnu pretragu
- Postavite broj rezultata (1-500)
- Pokrenite scraping

### 3. Job Status
- Real-time praćenje napretka
- Pregled preuzetih fajlova
- Statistika (pronađeno, uspešno, neuspešno)
- Auto-refresh svake 3 sekunde za aktivne job-ove

### 4. Moji Fajlovi
- Lista svih preuzetih PDF fajlova
- Filtriranje po kategoriji
- Pretraga po nazivu
- Download dugme za svaki fajl

### 5. Profil
- Korisnička statistika
- Omiljene kategorije
- Ukupna veličina fajlova
- Nedavna aktivnost

## 🛠️ Zaustavljanje i Pokretanje

### Zaustavljanje servera:
1. U terminalu pritisnite: **CTRL+C**

### Ponovno pokretanje:
```powershell
cd d:\ProjektiApp\pdfskrajpovanje
.\venv\Scripts\Activate.ps1
python app.py
```

## 📂 Struktura Projekta

```
pdfskrajpovanje/
├── app.py                  # Glavni Flask fajl
├── requirements.txt        # CLI zavisnosti
├── requirements-web.txt    # Web zavisnosti
├── config/
│   ├── settings.py        # Podešavanja
│   └── sources.py         # Izvori podataka
├── scrapers/
│   ├── base_scraper.py
│   ├── books_scraper.py
│   ├── research_scraper.py
│   └── magazine_scraper.py
├── web/
│   ├── database.py        # DB inicijalizacija
│   ├── models.py          # Modeli (User, Job, File)
│   ├── forms.py           # WTForms
│   └── tasks.py           # Background tasks
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── scrape.html
│   ├── job_status.html
│   ├── files.html
│   ├── profile.html
│   └── errors/
│       ├── 404.html
│       └── 500.html
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── main.js
│   └── favicon.ico
└── downloads/             # Preuzeti PDF fajlovi

```

## 🔧 Komande

### Flask CLI komande:
```powershell
# Inicijalizuj bazu (već urađeno automatski)
flask init-db-cmd

# Kreiraj admin korisnika
flask create-admin-user
```

## 💡 Tips & Tricks

1. **Real-time updates**: Job status stranica automatski osvežava podatke
2. **Filteri**: Na "Moji Fajlovi" možete filtrirati po kategoriji i pretražiti
3. **Keyboard shortcuts**: Browser shortcuts rade normalno
4. **Multiple tabs**: Možete otvoriti više tab-ova aplikacije
5. **Background jobs**: Scraping se izvršava asinhrono, možete zatvoriti stranicu

## 🐛 Debug Mode

Aplikacija radi u debug mode-u:
- Auto-reload na promene koda
- Detaljne error poruke
- Debug toolbar

Za production, koristite:
```powershell
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 📊 Baza Podataka

- **Tip**: SQLite
- **Fajl**: `pdf_scraper.db`
- **Lokacija**: `d:\ProjektiApp\pdfskrajpovanje\pdf_scraper.db`

### Tabele:
- `users` - Korisnički nalozi
- `scraping_jobs` - Scraping poslovi
- `downloaded_files` - Preuzeti fajlovi

## 🔐 Sigurnost

- Lozinke su heširane (bcrypt)
- Login sesije (Flask-Login)
- CSRF zaštita (Flask-WTF)
- @login_required dekoratori

## 📝 Napomene

1. Ovo je **development server** - ne koristiti u production-u
2. Za production koristiti Gunicorn/uWSGI + Nginx
3. Secret key promeniti za production
4. Database backup-ovati redovno

## ✨ Funkcionalnosti

✅ User authentication (login/register/logout)
✅ Dashboard sa statistikom
✅ Multi-category scraping (books, research, magazines)
✅ Real-time job status monitoring
✅ File management
✅ User profiles
✅ Error handling (404, 500)
✅ Responsive design (Bootstrap 5)
✅ Auto-open browser
✅ Background task execution
✅ API endpoints
✅ Form validation

## 🎯 Sledeći Koraci

1. Registrujte se na stranici Register
2. Pokrenite prvi scraping job
3. Pratite napredak na Job Status stranici
4. Preuzmite PDF fajlove

---

**Pitanja ili problemi?** Kontaktirajte podršku ili pogledajte log fajlove.
