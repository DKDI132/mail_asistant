from fastapi import FastAPI
import controler
from database import init_db
import asyncio
from services.scheduler import scheduler
app = FastAPI()
@app.on_event("startup")
def startup():
    init_db()
    asyncio.create_task(scheduler())
app.include_router(controler.router)

