# PDF Scraper - Kompletna Aplikacija ✅

## 🎉 Aplikacija je uspešno kreirana!

### 📁 Struktura Projekta

```
pdfskrajpovanje/
│
├── 📂 config/                  # Konfiguracija
│   ├── __init__.py            # Init fajl
│   ├── settings.py            # Globalne postavke
│   └── sources.py             # Konfiguracija izvora (arXiv, Gutenberg, itd.)
│
├── 📂 scrapers/               # Scraping moduli
│   ├── __init__.py           
│   ├── base_scraper.py       # Bazna klasa za sve scrapere
│   ├── books_scraper.py      # Scraper za knjige
│   ├── research_scraper.py   # Scraper za naučne radove
│   └── magazine_scraper.py   # Scraper za časopise
│
├── 📂 utils/                  # Pomoćni moduli
│   ├── __init__.py
│   ├── logger.py             # Logging sa Rich formatiranjem
│   ├── downloader.py         # Async PDF downloader
│   └── validators.py         # Validacija URL-ova i PDF-ova
│
├── 📂 ui/                     # Korisnički interfejs
│   ├── __init__.py
│   └── menu.py               # Interaktivni meni sa Rich
│
├── 📂 venv/                   # Python virtualno okruženje
├── 📂 storage/                # Crawlee storage
├── 📂 logs/                   # Log fajlovi
├── 📂 downloaded_pdfs/        # Preuzeti PDF-ovi (organizovano po kategorijama)
│   ├── books/
│   ├── research/
│   ├── magazines/
│   └── documents/
│
├── 📄 main.py                 # Glavni ulazni fajl
├── 📄 example.py              # Primer upotrebe
├── 📄 test_basic.py           # Osnovni testovi
├── 📄 requirements.txt        # Python zavisnosti
├── 📄 .env                    # Environment varijable
├── 📄 .env.example            # Primer .env fajla
├── 📄 .gitignore              # Git ignore fajl
├── 📄 README.md               # Glavna dokumentacija
├── 📄 QUICKSTART.md           # Brzi vodič
└── 📄 setup.ps1               # Setup skripta
```

## 🚀 Glavne Funkcionalnosti

### ✅ Implementirano

1. **Crawlee-Python Framework**
   - Koristi najnoviju verziju Crawlee (1.0.0)
   - Playwright browser za dinamički scraping
   - Async operacije za bolje performanse

2. **Kategorije Dokumenata**
   - 📚 Knjige (Project Gutenberg, Open Library)
   - 🔬 Naučni radovi (arXiv, PubMed Central, SSRN)
   - 📰 Časopisi (Internet Archive)
   - 📄 Custom dokumenti

3. **Automatsko Preuzimanje**
   - Async download sa kontrolom konkurentnosti
   - Retry mehanizam
   - Validacija PDF fajlova
   - Automatsko organizovanje po kategorijama

4. **Interaktivni UI**
   - Rich formatiranje u terminalu
   - Boje i tabele
   - Progress tracking
   - Intuitivne poruke

5. **Command Line Interface**
   - Argumenti za direktno pokretanje
   - Fleksibilna konfiguracija
   - Help komande

6. **Logging i Statistika**
   - Detaljni logovi u `logs/scraper.log`
   - Console output sa Rich
   - Statistika preuzimanja

## 🎯 Podržani Izvori

### Naučni Radovi
- **arXiv** - Fizika, matematika, računarstvo
- **PubMed Central** - Biomedicina
- **SSRN** - Društvene nauke

### Knjige
- **Project Gutenberg** - Knjige u javnom domenu
- **Open Library** - Otvorena biblioteka

### Časopisi
- **Internet Archive** - Digitalni arhiv

### Custom
- Mogućnost dodavanja bilo kog URL-a

## 💻 Kako Koristiti

### Osnovni Primeri

```powershell
# Interaktivni mod
python main.py --interactive

# Preuzimanje naučnih radova
python main.py --category research --source "arXiv" --query "AI" --limit 10

# Preuzimanje knjiga
python main.py --category books --source "Project Gutenberg" --query "fiction"

# Custom URL
python main.py --url "https://example.com/pdfs" --limit 20
```

### Napredna Konfiguracija

Uredi `.env` fajl:
```env
MAX_CONCURRENT_DOWNLOADS=5    # Broj istovremenih preuzimanja
DOWNLOAD_TIMEOUT=600          # Timeout u sekundama
OUTPUT_DIR=./moji_pdf         # Custom output direktorijum
```

## 🔧 Tehnologije

- **Python 3.8+**
- **Crawlee 1.0.0** - Web scraping framework
- **Playwright** - Browser automation
- **aiohttp** - Async HTTP client
- **Rich** - Terminal formatting
- **BeautifulSoup** - HTML parsing
- **lxml** - XML/HTML parser

## 📊 Performanse

- ⚡ Async operacije za brze downloadove
- 🎯 Kontrola konkurentnosti (default: 3 simultana)
- 🔄 Automatski retry pri greškama
- 💾 Efikasno skladištenje

## 🛡️ Validacije

- ✓ URL validacija
- ✓ PDF format provera (magic bytes)
- ✓ Veličina fajla check
- ✓ Content-Type provera

## 📝 Logovanje

Logovi se čuvaju na 2 nivoa:
1. **Console** - Lepo formatirano sa Rich (INFO level)
2. **File** - Detaljni logovi u `logs/scraper.log` (DEBUG level)

## 🎨 Dodavanje Novih Izvora

1. Otvori `config/sources.py`
2. Dodaj novi `Source` objekat
3. Definiši CSS selektore
4. Gotovo!

Primer:
```python
Source(
    name="Novi Izvor",
    url="https://example.com",
    source_type=SourceType.RESEARCH,
    description="Opis",
    selectors={
        "search_url": "https://example.com/search?q={query}",
        "pdf_link": "a.download-pdf",
        "title": "h1.title",
    }
)
```

## 🐛 Testiranje

```powershell
# Osnovni test
python test_basic.py

# Primer scraping-a
python example.py
```

## 📦 Deploymentgung

Aplikacija je spremna za:
- Windows (testirano)
- Linux (trebalo bi da radi)
- macOS (trebalo bi da radi)

## 🎓 Učenje i Prilagođavanje

Aplikacija je dizajnirana da bude:
- **Modularna** - Lako dodavanje novih scrapers-a
- **Proširiva** - Custom sources i kategorije
- **Čitljiva** - Dobro dokumentovan kod
- **Testabilna** - Jasna struktura za testove

## 🚀 Sledeći Koraci

Možete dodati:
- [ ] Web UI (Flask/FastAPI)
- [ ] Database za metadata (SQLite)
- [ ] Scheduled scraping (APScheduler)
- [ ] Email notifikacije
- [ ] Docker container
- [ ] API endpoints
- [ ] PDF text extraction (PyPDF2)
- [ ] Full-text search (Elasticsearch)

## 📄 Licenca

MIT License - Slobodno koristite i menjajte!

## 🤝 Kontribucije

Pull requests su dobrodošli!

---

**✨ Uživajte u scraping-u! ✨**
