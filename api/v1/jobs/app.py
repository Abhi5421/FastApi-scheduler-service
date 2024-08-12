from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from api.v1.jobs.utility import get_jobs_list, get_job, create_job
from database.connection import get_db
from api.v1.jobs.schema import *
from typing import List

router = APIRouter()


@router.get("/jobs-list", response_model=List[Job])
async def endpoint_list_jobs(
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db)
):
    try:
        jobs = await get_jobs_list(db=db, skip=skip, limit=limit)
        return jobs
    except Exception as e:
        return JSONResponse(content={'status': False, 'status_code': 500, 'detail': str(e)},
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/jobs/{job_id}", response_model=Job)
async def endpoint_get_job(job_id: int, db: Session = Depends(get_db)):
    try:
        response = await get_job(db=db, job_id=job_id)
        if response is None:
            raise HTTPException(status_code=404, detail="Job not found")
        return response
    except Exception as e:
        return JSONResponse(content={'status': False, 'status_code': 500, 'detail': str(e)},
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post("/create-job", response_model=Job)
async def endpoint_create_job(job: JobCreate, db: Session = Depends(get_db)):
    try:
        response = await create_job(db=db, job=job)
        return response
    except Exception as e:
        return JSONResponse(content={'status': False, 'status_code': 500, 'detail': str(e)},
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)