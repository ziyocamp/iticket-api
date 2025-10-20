from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import users
app = FastAPI(title="ITicket API", version="0.1.0")

from app.db import models, database
from app.routers import users

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="iTicket API")

app.include_router(users.router)



from app.db.init_db import create_tables
# from app.routers.users import router as users_router

create_tables()

app = FastAPI(
    title="ITicket API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(users_router)
