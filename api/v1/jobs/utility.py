from sqlalchemy.orm import Session
from api.v1.jobs.model import Job
from api.v1.jobs.schema import JobCreate
from utils.scheduler import schedule_jobs
from utils.celery.tasks import schedule_job_using_celery


async def get_jobs_list(db: Session, skip: int = 0, limit: int = 10):
    response = db.query(Job).offset(skip).limit(limit).all()
    return response


async def get_job(db: Session, job_id: int):
    return db.query(Job).filter(Job.id == job_id).first()


async def create_job(db: Session, job: JobCreate):
    db_job = Job(name=job.name,
                 description=job.description,
                 schedule_interval=job.schedule_interval,
                 status=job.status,
                 active=job.active
                 )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)

    # using apscheduler
    schedule_jobs()

    # using celery
    # schedule_job_using_celery(db_job)

    return db_job
