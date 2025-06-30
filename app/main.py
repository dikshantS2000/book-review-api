from fastapi import FastAPI
from app.route import router
from app.database import init_db

app = FastAPI(title="Book Review API")

init_db()
app.include_router(router)
