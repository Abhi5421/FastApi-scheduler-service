from celery import Celery
from celery.schedules import crontab
from database.config import settings

celery_app = Celery(
    "scheduler",
    broker=settings.celery_broker_url,
    backend=settings.celery_backend_url,
)

celery_app.conf.beat_schedule = {
    'check-jobs-every-minute': {
        'task': 'tasks_scheduler.schedule_jobs',
        'schedule': crontab(minute='*/1'),
    },
}
