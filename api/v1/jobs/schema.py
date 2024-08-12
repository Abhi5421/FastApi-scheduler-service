from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class JobBase(BaseModel):
    name: str
    description: Optional[str] = None
    active: bool
    status: str


class JobCreate(JobBase):
    schedule_interval: str


class Job(JobBase):
    id: int
    last_run: Optional[datetime] = None
    next_run: Optional[datetime] = None

    class Config:
        from_attribute = True
