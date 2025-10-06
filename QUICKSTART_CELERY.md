# 🚀 QUICK START - CELERY VERSION

## Najbrži način da pokrenete projekat sa Celery-jem

### 📋 Prerequisiti

1. **Python 3.8+** instaliran
2. **Redis** instaliran ([Download](https://github.com/microsoftarchive/redis/releases) ili koristite Docker)
3. **Git** (opcionalno)

### ⚡ 3 Koraka do pokretanja

#### 1️⃣ Instalirajte zavisnosti

```powershell
pip install -r requirements.txt
pip install -r requirements-web.txt
```

#### 2️⃣ Kopirajte .env fajl

```powershell
Copy-Item .env.example .env
```

Ili manuelno: kopirajte `.env.example` u `.env`

#### 3️⃣ Pokrenite sve servise odjednom

```powershell
.\start_all.ps1
```

**Skripta automatski pokreće:**
- ✅ Redis server
- ✅ Celery worker
- ✅ Flask web aplikaciju

### 🌐 Pristupite aplikaciji

Otvorite browser na: **http://localhost:5000**

---

## 🔧 Manuelno pokretanje (ako preferite kontrolu)

Ako želite da pokrenete svaki servis posebno:

### Terminal 1: Redis
```powershell
redis-server
# Ili: .\start_redis.ps1
```

### Terminal 2: Celery Worker
```powershell
.\start_celery.ps1
# Ili manuelno:
# celery -A celery_config.celery_app worker --loglevel=info --pool=solo
```

### Terminal 3: Flask App
```powershell
python app.py
```

---

## 📊 (Opcionalno) Pokrenite Flower Monitoring

Flower je web interface za praćenje Celery task-ova:

```powershell
.\start_flower.ps1
```

Pristup: **http://localhost:5555**

---

## ✅ Verifikacija

Proverite da li sve radi:

```powershell
python test_celery.py
```

Trebalo bi da vidite:
```
✅ Celery is connected!
   Active workers: 1
```

---

## 🆘 Troubleshooting

### ❌ "Redis connection refused"
**Rešenje:** Redis nije pokrenut. Pokrenite `redis-server` ili `.\start_redis.ps1`

### ❌ "No Celery workers found"
**Rešenje:** Worker nije pokrenut. Pokrenite `.\start_celery.ps1`

### ❌ "Module 'celery' not found"
**Rešenje:** Instalirajte zavisnosti: `pip install -r requirements-web.txt`

---

## 📚 Dodatne informacije

Za detaljniju dokumentaciju pogledajte:
- **[CELERY_SETUP.md](CELERY_SETUP.md)** - Kompletna Celery dokumentacija
- **[WEB_SETUP.md](WEB_SETUP.md)** - Web aplikacija setup
- **[README.md](README.md)** - Glavni README

---

## 🎉 Gotovo!

Sada možete:
1. Registrovati se na **http://localhost:5000/register**
2. Prijaviti se
3. Pokrenuti scraping job-ove
4. Pratiti napredak u realnom vremenu

**Background task processing radi! 🚀**
