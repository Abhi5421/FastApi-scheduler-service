from fastapi import FastAPI,Request
import uvicorn
import time
from api.v1.jobs.app import router as jobs
from database.connection import Base, engine
from utils.logger import create_logger

logging = create_logger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI(docs_url="/api/docs")
app.include_router(jobs)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    logging.info(f"Incoming Request: {request.method} {request.url}")
    response = await call_next(request)
    if response.status_code != 200:
        logging.error(f"Status Code: {response.status_code}")
    process_time = (time.time() - start_time) * 1000
    logging.info(f"process_time: {process_time}")
    return response


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8005)
