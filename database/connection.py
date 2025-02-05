from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from database.config import settings

DATABASE_URL = settings.mysql_url

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
