# PDF Skrejper Aplikacija

Aplikacija za automatsko preuzimanje PDF dokumenata sa različitih izvora korišćenjem Crawlee-Python framework-a.

## 🚀 Karakteristike

- ✅ Scraping različitih tipova dokumenata (knjige, časopisi, naučni radovi, itd.)
- ✅ Interaktivni korisnički interfejs za izbor kategorija
- ✅ Automatsko preuzimanje i organizovanje PDF fajlova
- ✅ Podrška za više izvora istovremeno
- ✅ Napredna obrada grešaka i retry mehanizmi
- ✅ Logging i progress tracking
- ✅ Konfigurisanje različitih ciljnih sajtova

## 📦 Instalacija

### 1. Kreiranje virtualnog okruženja

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. Instalacija zavisnosti

```powershell
pip install -r requirements.txt
```

### 3. Instalacija Playwright browsera

```powershell
playwright install
```

### 4. Konfiguracija

```powershell
copy .env.example .env
```

Uredi `.env` fajl prema svojim potrebama.

## 🎯 Upotreba

### Osnovno pokretanje

```powershell
python main.py
```

### Direktan izbor kategorije

```powershell
# Knjige
python main.py --category books

# Naučni članci
python main.py --category research

# Časopisi
python main.py --category magazines
```

### Dodatne opcije

```powershell
# Sa specifičnim izvorom
python main.py --category books --source arxiv

# Sa limitom rezultata
python main.py --category research --limit 50

# Sa custom output direktorijumom
python main.py --category books --output ./moje_knjige
```

## 🎯 Verzije Projekta

Projekat ima **2 načina rada**:

### 1. 🌐 Web Aplikacija sa Celery (Preporučeno za produkciju)
- Profesionalni background task processing
- Non-blocking scraping operacije
- Redis queue management
- Real-time progress tracking
- 📖 Setup: **[QUICKSTART_CELERY.md](QUICKSTART_CELERY.md)**

### 2. 🖥️ CLI Verzija (Jednostavnija)
- Direktno pokretanje iz terminala
- Bez Redis/Celery zavisnosti
- Odlično za testiranje
- 📖 Setup: **[QUICKSTART.md](QUICKSTART.md)**

---

## � Struktura Projekta

```
pdfskrajpovanje/
├── main.py                 # Glavni ulazni fajl
├── config/
│   ├── __init__.py
│   ├── settings.py        # Globalne postavke
│   └── sources.py         # Konfiguracija izvora
├── scrapers/
│   ├── __init__.py
│   ├── base_scraper.py    # Bazna klasa za scrapere
│   ├── books_scraper.py   # Scraper za knjige
│   ├── research_scraper.py # Scraper za naučne radove
│   └── magazine_scraper.py # Scraper za časopise
├── utils/
│   ├── __init__.py
│   ├── downloader.py      # PDF download manager
│   ├── logger.py          # Logging utilities
│   └── validators.py      # Validacija URL-ova i fajlova
├── ui/
│   ├── __init__.py
│   └── menu.py            # Interaktivni meni
└── requirements.txt
```

## 🎨 Primeri izvora

Aplikacija podržava scraping sa:

- **arXiv** - Naučni radovi
- **Project Gutenberg** - Besplatne knjige
- **PubMed Central** - Medicinski članci
- **Custom izvori** - Dodaj svoje izvore u `config/sources.py`

## 📝 Dodavanje novog izvora

1. Kreiraj novi scraper u `scrapers/` direktorijumu
2. Naslijedi `BaseScraper` klasu
3. Implementiraj `scrape()` metod
4. Dodaj izvor u `config/sources.py`

```python
from scrapers.base_scraper import BaseScraper

class MyCustomScraper(BaseScraper):
    async def scrape(self):
        # Tvoja logika
        pass
```

## 🐛 Troubleshooting

### Playwright greška

```powershell
playwright install
```

### Timeout greške

Povećaj `DOWNLOAD_TIMEOUT` u `.env` fajlu.

## 📄 Licenca

MIT License

## 🤝 Doprinos

Pull requests su dobrodošli!
