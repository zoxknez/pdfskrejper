# 🚀 CELERY SETUP - PDF SCRAPER

## 📋 Pregled

Ovaj projekat koristi **Celery** za asinhrono izvršavanje scraping task-ova. Celery omogućava:
- ✅ Non-blocking izvršavanje poslova
- ✅ Task queue management
- ✅ Retry mehanizam
- ✅ Progress tracking
- ✅ Skalabilnost

## 🔧 Instalacija

### 1. Instalirajte Redis

**Redis** je broker za Celery task queue.

#### Windows:
- **Opcija A - Direktna instalacija:**
  ```powershell
  # Preuzmite Redis za Windows
  # https://github.com/microsoftarchive/redis/releases
  # Instalirajte i dodajte u PATH
  ```

- **Opcija B - Docker (Preporučeno):**
  ```powershell
  docker run -d -p 6379:6379 --name redis redis:alpine
  ```

- **Opcija C - WSL2:**
  ```bash
  sudo apt-get update
  sudo apt-get install redis-server
  sudo service redis-server start
  ```

#### Linux/Mac:
```bash
# Ubuntu/Debian
sudo apt-get install redis-server

# macOS
brew install redis
brew services start redis
```

### 2. Instalirajte Python zavisnosti

```powershell
pip install -r requirements-web.txt
```

Ovo instalira:
- `celery>=5.3.4`
- `redis>=5.0.1`
- Sve ostale zavisnosti

## 🚀 Pokretanje

### Korak 1: Pokrenite Redis

```powershell
# Ako ste instalirali direktno:
redis-server

# Ako koristite Docker:
docker start redis

# Ili koristite našu skriptu:
.\start_redis.ps1
```

Verifikujte da Redis radi:
```powershell
redis-cli ping
# Trebalo bi da vrati: PONG
```

### Korak 2: Pokrenite Celery Worker

U **NOVOM terminalu**:

```powershell
.\start_celery.ps1
```

Ili manuelno:
```powershell
celery -A celery_config.celery_app worker --loglevel=info --pool=solo --concurrency=2
```

### Korak 3: Pokrenite Flask aplikaciju

U **DRUGOM terminalu**:

```powershell
python app.py
```

## 📊 Arhitektura

```
┌─────────────┐
│ Flask App   │  (Web Server - Port 5000)
│ (app.py)    │
└──────┬──────┘
       │
       │ Submits task
       ▼
┌─────────────┐
│   Redis     │  (Message Broker - Port 6379)
│   Queue     │
└──────┬──────┘
       │
       │ Pulls task
       ▼
┌─────────────┐
│   Celery    │  (Worker Process)
│   Worker    │  Izvršava scraping
└─────────────┘
```

## 🔄 Kako radi?

1. **Korisnik pokreće scraping** na web stranici
2. Flask kreira `ScrapingJob` u bazi i **dodaje task u Redis queue**
3. **Celery worker** povlači task iz queue-a i počinje scraping
4. Worker **ažurira status** job-a u bazi tokom izvršavanja
5. Korisnik može **pratiti progress** u realnom vremenu

## 📝 Celery Tasks

### `scrape_task`
Glavni task za scraping operacije.

```python
from web.celery_tasks import scrape_task

# Pokreni task
task = scrape_task.delay(job_id=123)

# Proveri status
task.ready()  # True ako je gotovo
task.status   # 'PENDING', 'STARTED', 'SUCCESS', 'FAILURE'
task.result   # Rezultat task-a
```

### `update_job_progress`
Task za ažuriranje progresa.

```python
from web.celery_tasks import update_job_progress

update_job_progress.delay(job_id=123, progress=50, status='running')
```

### `cleanup_old_jobs`
Periodičan task za čišćenje starih poslova (za Celery Beat).

## 🛠️ Konfiguracija

### `celery_config.py`

Glavne postavke:
```python
REDIS_URL = 'redis://localhost:6379/0'  # Redis konekcija

# Task routing
task_routes = {
    'web.celery_tasks.scrape_task': {'queue': 'scraping'},
    'web.celery_tasks.download_task': {'queue': 'downloads'},
}

# Limits
task_time_limit = 3600  # 1 sat max
task_soft_time_limit = 3300  # 55 minuta soft limit
```

### Environment Variables (.env)

```env
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key-here
```

## 🔍 Monitoring

### Flower - Celery Monitoring Tool

Instalirajte Flower za GUI monitoring:

```powershell
pip install flower
```

Pokrenite:
```powershell
celery -A celery_config.celery_app flower --port=5555
```

Pristupite: http://localhost:5555

## 🐛 Debugging

### Provera Redis konekcije

```powershell
redis-cli ping
# Očekivani odgovor: PONG
```

### Provera Celery worker-a

```powershell
celery -A celery_config.celery_app inspect active
```

### Logovi

Celery worker ispisuje detaljne logove:
- Task start/stop
- Greške
- Progress

## 📦 Production Deployment

Za produkciju:

1. **Koristite Supervisor/systemd** za automatsko pokretanje worker-a
2. **Konfigurirajte više worker-a** za skalabilnost
3. **Postavite Redis persistence**
4. **Koristite Celery Beat** za periodic tasks

### Pokretanje više worker-a:

```powershell
# Worker 1 - Scraping queue
celery -A celery_config.celery_app worker -Q scraping -n worker1@%h

# Worker 2 - Downloads queue
celery -A celery_config.celery_app worker -Q downloads -n worker2@%h
```

## 🔒 Security

- **Ne hardkodujte SECRET_KEY** - koristite environment varijable
- **Zaštitite Redis** sa password-om u produkciji
- **Rate limit** task-ove ako je potrebno

## ❓ FAQ

**Q: Zašto Redis?**
A: Redis je brz, jednostavan i popularan message broker za Celery.

**Q: Mogu li koristiti RabbitMQ umesto Redis-a?**
A: Da! Promenite `REDIS_URL` u `celery_config.py`.

**Q: Koliko worker-a mi treba?**
A: Zavisi od opterećenja. Počnite sa 2-4 worker-a.

**Q: Šta ako Redis padne?**
A: Task-ovi će čekati dok se Redis ne restartuje. Nema gubitka podataka.

## 🆘 Troubleshooting

### Problem: "Connection refused" greška

**Rešenje:** Redis nije pokrenut. Pokrenite `redis-server`.

### Problem: Worker se ne pokreće

**Rešenje:** Proverite:
1. Da li je Redis pokrenut?
2. Da li ste instalirali `celery` i `redis` pakete?
3. Proveru logove za detaljnije greške

### Problem: Task-ovi se ne izvršavaju

**Rešenje:**
1. Proverite da li worker radi: `celery -A celery_config.celery_app inspect active`
2. Proverite Redis queue: `redis-cli LLEN celery`

## 📚 Dodatni resursi

- [Celery dokumentacija](https://docs.celeryq.dev/)
- [Redis dokumentacija](https://redis.io/documentation)
- [Flask + Celery tutorial](https://blog.miguelgrinberg.com/post/using-celery-with-flask)

---

**🎉 Gotovo! Sada imate professional-grade background task processing!**
