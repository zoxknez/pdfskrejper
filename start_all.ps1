# 🚀 ALL-IN-ONE START SCRIPT
# Ova skripta pokreće Redis, Celery Worker i Flask app u zasebnim prozorima

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🚀 PDF SCRAPER - ALL-IN-ONE STARTUP" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 1. Proveri da li .env fajl postoji
if (-not (Test-Path ".env")) {
    Write-Host "⚠️  .env fajl ne postoji!" -ForegroundColor Yellow
    Write-Host "Kreiram iz .env.example..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "✅ .env kreiran! Proverite i prilagodite postavke." -ForegroundColor Green
    Write-Host ""
}

# 2. Proveri zavisnosti
Write-Host "📦 Proveravam zavisnosti..." -ForegroundColor Yellow

$pipList = pip list 2>$null
if ($pipList -notmatch "celery") {
    Write-Host "⚠️  Celery nije instaliran!" -ForegroundColor Red
    Write-Host "Instaliram zavisnosti..." -ForegroundColor Yellow
    pip install -r requirements-web.txt
    Write-Host "✅ Zavisnosti instalirane!" -ForegroundColor Green
    Write-Host ""
}

# 3. Start Redis
Write-Host "📡 Pokrećem Redis..." -ForegroundColor Yellow

$redisProcess = Get-Process redis-server -ErrorAction SilentlyContinue
if (-not $redisProcess) {
    $redisPath = Get-Command redis-server -ErrorAction SilentlyContinue
    
    if ($redisPath) {
        Start-Process powershell -ArgumentList "-NoExit", "-Command", ".\start_redis.ps1" -WindowStyle Normal
        Write-Host "✅ Redis pokrenut u novom prozoru" -ForegroundColor Green
        Start-Sleep -Seconds 2
    } else {
        Write-Host "❌ Redis nije instaliran!" -ForegroundColor Red
        Write-Host "Molim vas instalirajte Redis:" -ForegroundColor Yellow
        Write-Host "  - Download: https://github.com/microsoftarchive/redis/releases" -ForegroundColor White
        Write-Host "  - Ili Docker: docker run -d -p 6379:6379 redis" -ForegroundColor White
        Write-Host ""
        Read-Host "Pritisnite Enter nakon instalacije Redis-a"
    }
} else {
    Write-Host "✅ Redis već radi" -ForegroundColor Green
}

# 4. Start Celery Worker
Write-Host ""
Write-Host "🔧 Pokrećem Celery Worker..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", ".\start_celery.ps1" -WindowStyle Normal
Write-Host "✅ Celery Worker pokrenut u novom prozoru" -ForegroundColor Green

# 5. Čekaj malo da se worker podigne
Write-Host ""
Write-Host "⏳ Čekam da se Celery worker inicijalizuje..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

# 6. Start Flask App
Write-Host ""
Write-Host "🌐 Pokrećem Flask aplikaciju..." -ForegroundColor Yellow
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "✅ SVE JE POKRENUTO!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "📍 Servisi:" -ForegroundColor Cyan
Write-Host "  • Flask Web:    http://localhost:5000" -ForegroundColor White
Write-Host "  • Redis:        localhost:6379" -ForegroundColor White
Write-Host "  • Celery Worker: Radi u pozadini" -ForegroundColor White
Write-Host ""
Write-Host "💡 Opcionalno pokrenite Flower monitoring:" -ForegroundColor Yellow
Write-Host "   .\start_flower.ps1" -ForegroundColor White
Write-Host ""
Write-Host "⚠️  Za zaustavljanje zatvorite sve prozore ili pritisnite CTRL+C" -ForegroundColor Yellow
Write-Host ""

# Pokreni Flask
python app.py
