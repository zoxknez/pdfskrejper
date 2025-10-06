# QUICK START GUIDE - PDF Scraper

## 📚 Brzi vodič za korišćenje

### 1. Prvi put - Instalacija

```powershell
# Otvorite PowerShell u direktorijumu projekta
cd d:\ProjektiApp\pdfskrajpovanje

# Kreirajte virtualno okruženje
python -m venv venv

# Aktivirajte virtualno okruženje
.\venv\Scripts\Activate.ps1

# Instalirajte zavisnosti
pip install -r requirements.txt

# Instalirajte Playwright browser
playwright install chromium
```

### 2. Pokretanje aplikacije

#### Interaktivni mod (preporučeno za početnike)

```powershell
# Aktivirajte virtualno okruženje
.\venv\Scripts\Activate.ps1

# Pokrenite aplikaciju
python main.py
```

Aplikacija će vas provesti kroz interaktivni meni gde možete:
- Izabrati kategoriju dokumenata (knjige, naučni radovi, časopisi)
- Izabrati izvor (arXiv, Project Gutenberg, itd.)
- Uneti pretragu (keywords)
- Podesiti limit rezultata

#### Command line mod (za napredne korisnike)

```powershell
# Aktivirajte virtualno okruženje
.\venv\Scripts\Activate.ps1

# Preuzmi naučne radove sa arXiv-a
python main.py --category research --source "arXiv" --query "machine learning" --limit 10

# Preuzmi knjige sa Gutenberg-a
python main.py --category books --source "Project Gutenberg" --query "science fiction" --limit 5

# Custom URL scraping
python main.py --url "https://example.com/pdfs" --limit 20
```

### 3. Gde se čuvaju preuzeti fajlovi?

Fajlovi se automatski organizuju u:
```
downloaded_pdfs/
├── books/          # Knjige
├── research/       # Naučni radovi
├── magazines/      # Časopisi
└── documents/      # Ostali dokumenti
```

### 4. Primeri korišćenja

#### Primer 1: Preuzimanje Python tutoriala

```powershell
python main.py --category research --source "arXiv" --query "python programming" --limit 15
```

#### Primer 2: Preuzimanje knjiga iz javnog domena

```powershell
python main.py --category books --source "Project Gutenberg" --query "shakespeare" --limit 10
```

#### Primer 3: Interaktivni mod

```powershell
python main.py --interactive
```

### 5. Rešavanje problema

#### Problem: "playwright nije prepoznat"
**Rešenje:**
```powershell
.\venv\Scripts\Activate.ps1
playwright install chromium
```

#### Problem: "ModuleNotFoundError"
**Rešenje:**
```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

#### Problem: Timeout greške
**Rešenje:**
Povećajte timeout u `.env` fajlu:
```
DOWNLOAD_TIMEOUT=600
```

### 6. Napredne opcije

#### Podešavanje konkurentnosti

U `.env` fajlu:
```env
MAX_CONCURRENT_DOWNLOADS=5  # Broj istovremenih preuzimanja
```

#### Prilagođavanje output direktorijuma

```powershell
python main.py --category books --output "C:\Moje Knjige"
```

#### Povećanje broja rezultata

```powershell
python main.py --category research --limit 100
```

### 7. Logovi

Logovi se čuvaju u `logs/scraper.log` fajlu za debugging.

### 8. Dodavanje novih izvora

Otvorite `config/sources.py` i dodajte novi izvor:

```python
Source(
    name="Moj Izvor",
    url="https://example.com",
    source_type=SourceType.BOOKS,
    description="Opis izvora",
    selectors={
        "search_url": "https://example.com/search?q={query}",
        "pdf_link": "a[href$='.pdf']",
    }
)
```

### 9. Deaktivacija virtualnog okruženja

```powershell
deactivate
```

### 10. Pomoć i dokumentacija

Za detaljniju dokumentaciju, pogledajte `README.md` fajl.

Za listu komandi:
```powershell
python main.py --help
```

---

## 🎯 Brze komande

| Akcija | Komanda |
|--------|---------|
| Aktiviraj venv | `.\venv\Scripts\Activate.ps1` |
| Pokreni app | `python main.py` |
| Interaktivni mod | `python main.py --interactive` |
| arXiv scraping | `python main.py --category research --source "arXiv" --query "AI" --limit 10` |
| Pomoć | `python main.py --help` |
| Deaktiviraj venv | `deactivate` |

---

**💡 TIP**: Uvek aktivirajte virtualno okruženje pre pokretanja aplikacije!
