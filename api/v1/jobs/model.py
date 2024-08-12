from sqlalchemy import Column, Integer, VARCHAR, DateTime, Boolean
from database.connection import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(VARCHAR(256), index=True)
    description = Column(VARCHAR(256), nullable=True)
    last_run = Column(DateTime, nullable=True)
    next_run = Column(DateTime, nullable=True)
    schedule_interval = Column(VARCHAR(256), nullable=True)
    status = Column(VARCHAR(256), nullable=True)
    active = Column(Boolean, default=True, nullable=True)
