from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.triggers.cron import CronTrigger
from database.connection import SessionLocal
from datetime import datetime, timedelta
from api.v1.jobs.model import Job
from database.connection import engine

jobstores = {
    'default': SQLAlchemyJobStore(engine=engine)
}

scheduler = BackgroundScheduler(jobstores=jobstores)
scheduler.start()


def construct_cron_expression(interval: str) -> str:
    if interval == "daily":
        return "0 0 * * *"
    elif interval == "weekly":
        return "0 0 * * 0"
    elif interval == "every_minute":
        return "* * * * *"
    return ""


def schedule_jobs():
    with SessionLocal() as db:
        jobs = db.query(Job).all()
        for job in jobs:
            if job.active and job.status != "completed":
                cron_expression = construct_cron_expression(job.schedule_interval)
                if cron_expression:
                    scheduler.add_job(
                        execute_job,
                        CronTrigger.from_crontab(cron_expression),
                        args=[job.id],
                        id=str(job.id),
                        replace_existing=True
                    )


def calculate_next_run(interval: str) -> datetime:
    now = datetime.now()
    if interval == "daily":
        return now + timedelta(days=1)
    elif interval == "weekly":
        return now + timedelta(weeks=1)
    elif interval == "every_minute":
        return now + timedelta(minutes=1)
    return now + timedelta(days=7)


def execute_job(job_id: int):
    with SessionLocal() as db:
        job = db.query(Job).get(job_id)
        if job:
            job.last_run = datetime.now()
            job.next_run = calculate_next_run(job.schedule_interval)
            job.status = "completed"
            db.add(job)
            db.commit()
