"""Check database schema for scraping_jobs table"""
import sqlite3

conn = sqlite3.connect('instance/pdf_scraper.db')
cursor = conn.cursor()
cursor.execute('PRAGMA table_info(scraping_jobs)')
columns = cursor.fetchall()

print("\n📊 scraping_jobs TABLE SCHEMA:")
print("=" * 60)
for col in columns:
    print(f"  {col[0]:2d}. {col[1]:20s} {col[2]:15s} {'NULL' if not col[3] else 'NOT NULL'}")
print("=" * 60)
print(f"\n✅ Total columns: {len(columns)}")

# Check if celery_task_id exists
has_celery_task_id = any(col[1] == 'celery_task_id' for col in columns)
if has_celery_task_id:
    print("✅ celery_task_id column EXISTS!")
else:
    print("❌ celery_task_id column MISSING!")

conn.close()
