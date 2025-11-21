from fastapi import FastAPI
from .database import init_db
from .controllers import router as api_router

app = FastAPI(title="Users & Tasks API")


@app.on_event("startup")
def on_startup():
    init_db()


app.include_router(api_router)
