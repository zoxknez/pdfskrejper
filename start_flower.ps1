# Celery Flower Monitoring
# Pokreće Flower web interface za monitoring Celery task-ova

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🌸 CELERY FLOWER MONITORING" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "📊 Pokrećem Flower monitoring..." -ForegroundColor Yellow
Write-Host ""
Write-Host "Pristupite web interfejsu na: http://localhost:5555" -ForegroundColor Green
Write-Host ""

celery -A celery_config.celery_app flower --port=5555

Write-Host ""
Write-Host "Flower je zaustavljen." -ForegroundColor Red
