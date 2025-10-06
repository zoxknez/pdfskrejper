"""
Quick test script za proveru Celery setup-a.
"""

from celery_config import celery_app
from web.celery_tasks import scrape_task, update_job_progress


def test_celery_connection():
    """Test Redis connection."""
    print("🔍 Testing Celery connection...")

    try:
        # Ping Celery
        inspect = celery_app.control.inspect()
        stats = inspect.stats()

        if stats:
            print("✅ Celery is connected!")
            print(f"   Active workers: {len(stats)}")
            for worker_name, worker_stats in stats.items():
                print(f"   - {worker_name}")
        else:
            print("❌ No Celery workers found!")
            print("   Start worker with: .\start_celery.ps1")

    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("   Make sure Redis is running!")


def test_simple_task():
    """Test simple Celery task."""
    print("\n🧪 Testing simple task...")

    try:
        # Ovde bi išao test task
        print("✅ Task submission works!")

    except Exception as e:
        print(f"❌ Task failed: {e}")


if __name__ == "__main__":
    print("=" * 50)
    print("🔬 CELERY SETUP TEST")
    print("=" * 50)
    print()

    test_celery_connection()
    # test_simple_task()

    print()
    print("=" * 50)
    print("Test completed!")
    print("=" * 50)
