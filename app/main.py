from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db import models, database
from app.db.init_db import create_tables
from app.routers import users
app = FastAPI(
    title="ITicket API",
    version="0.1.0"
)

models.Base.metadata.create_all(bind=database.engine)
create_tables()

app.include_router(users.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
