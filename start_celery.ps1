# Celery Worker Start Script
# Ova skripta pokreće Celery worker za PDF Scraper

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🚀 PDF SCRAPER - CELERY WORKER" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Proveri da li je Redis pokrenut
Write-Host "📡 Proveravam Redis konekciju..." -ForegroundColor Yellow

$redisRunning = $false
try {
    $redisTest = Test-Connection -ComputerName localhost -Port 6379 -Count 1 -ErrorAction SilentlyContinue
    if ($redisTest) {
        $redisRunning = $true
    }
} catch {
    $redisRunning = $false
}

if (-not $redisRunning) {
    Write-Host "❌ Redis nije pokrenut!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Molim vas pokrenite Redis pre nego što startujete worker:" -ForegroundColor Yellow
    Write-Host "  - Na Windows-u: redis-server.exe" -ForegroundColor White
    Write-Host "  - Ili koristite Docker: docker run -d -p 6379:6379 redis" -ForegroundColor White
    Write-Host ""
    pause
    exit 1
}

Write-Host "✅ Redis je aktivan!" -ForegroundColor Green
Write-Host ""

# Pokreni Celery worker
Write-Host "🔧 Pokrećem Celery worker..." -ForegroundColor Yellow
Write-Host ""

# Celery worker komanda
celery -A celery_config.celery_app worker `
    --loglevel=info `
    --concurrency=2 `
    --pool=solo `
    --queues=scraping,downloads `
    --hostname=worker@%h

Write-Host ""
Write-Host "Worker je zaustavljen." -ForegroundColor Red
