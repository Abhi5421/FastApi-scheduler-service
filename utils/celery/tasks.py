from utils.celery.celery_config import celery_app
from datetime import datetime, timedelta
from api.v1.jobs.model import Job
from database.connection import SessionLocal


@celery_app.task
def execute_job(job_id: int):
    with SessionLocal() as db:
        job = db.query(Job).get(job_id)
        if job:
            print(f"Executing job {job_id}: {job.name}")
            job.last_run = datetime.now()
            job.next_run = calculate_next_run(job.schedule_interval)
            job.status = "completed"
            db.add(job)
            db.commit()


def calculate_next_run(interval: str) -> datetime:
    now = datetime.now()
    if interval == "daily":
        return now + timedelta(days=1)
    elif interval == "weekly":
        return now + timedelta(weeks=1)
    elif interval == "every_minute":
        return now + timedelta(minutes=1)
    return now + timedelta(days=7)


def construct_cron_expression(interval: str) -> str:
    if interval == "daily":
        return "0 0 * * *"
    elif interval == "weekly":
        return "0 0 * * 0"
    elif interval == "every_minute":
        return "* * * * *"
    return ""


def schedule_job_using_celery(job):
    cron_expression = construct_cron_expression(job.schedule_interval)
    if cron_expression:
        celery_app.add_periodic_task(
            cron_expression,
            execute_job(job.id),
            name=f'job_{job.id}'
        )
