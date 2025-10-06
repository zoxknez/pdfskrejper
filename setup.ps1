# PDF SCRAPER - Setup Script
Write-Host "========================================"
Write-Host "  PDF SCRAPER - Setup"
Write-Host "========================================"
Write-Host ""

# Check Python
Write-Host "Proveravam Python..."
python --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "Python nije pronadjen!"
    exit 1
}

# Create venv
Write-Host ""
Write-Host "Kreiram virtualno okruzenje..."
if (!(Test-Path "venv")) {
    python -m venv venv
}

# Activate venv
Write-Host "Aktiviram virtualno okruzenje..."
& .\venv\Scripts\Activate.ps1

# Upgrade pip
Write-Host ""
Write-Host "Azuriram pip..."
python -m pip install --upgrade pip

# Install dependencies
Write-Host ""
Write-Host "Instaliram zavisnosti..."
pip install -r requirements.txt

# Install Playwright
Write-Host ""
Write-Host "Instaliram Playwright browser..."
playwright install chromium

# Create directories
Write-Host ""
Write-Host "Kreiram direktorijume..."
New-Item -ItemType Directory -Force -Path "storage" | Out-Null
New-Item -ItemType Directory -Force -Path "downloaded_pdfs" | Out-Null
New-Item -ItemType Directory -Force -Path "logs" | Out-Null

# Done
Write-Host ""
Write-Host "Setup zavrsen!"
Write-Host ""
Write-Host "Pokretanje:"
Write-Host "  .\venv\Scripts\Activate.ps1"
Write-Host "  python main.py"
Write-Host ""
