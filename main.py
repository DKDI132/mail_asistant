from fastapi import FastAPI
import controler
from database import init_db
app = FastAPI()
@app.on_event("startup")
def startup():
    init_db()
app.include_router(controler.router)

