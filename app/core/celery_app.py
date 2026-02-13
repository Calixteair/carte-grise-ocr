from celery import Celery

from app.core.config import settings

celery_app = Celery(
    "carte_grise_ocr",
    broker=settings.REDIS_BROKER_URL,
    backend=settings.REDIS_BACKEND_URL
)

celery_app.conf.update(
    task_track_started=True,
    task_time_limit=3600, # 1 hour
    broker_connection_retry_on_startup=True,
    include=['app.worker.tasks']
)

# Optional: Load task modules
# celery_app.autodiscover_tasks(['app.worker'])
