# Start Redis (ako nije pokrenut)
Write-Host "Starting Redis..." -ForegroundColor Cyan

# Proveri da li Redis postoji
$redisPath = Get-Command redis-server -ErrorAction SilentlyContinue

if ($redisPath) {
    Start-Process redis-server -WindowStyle Minimized
    Write-Host "✅ Redis started" -ForegroundColor Green
} else {
    Write-Host "❌ Redis nije instaliran!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Instalirajte Redis:" -ForegroundColor Yellow
    Write-Host "  Option 1: Preuzmite sa https://github.com/microsoftarchive/redis/releases" -ForegroundColor White
    Write-Host "  Option 2: Koristite Docker: docker run -d -p 6379:6379 redis" -ForegroundColor White
    Write-Host "  Option 3: Koristite WSL2 i instalirajte Redis u Linux-u" -ForegroundColor White
    Write-Host ""
    pause
}
