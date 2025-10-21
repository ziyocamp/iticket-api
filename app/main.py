from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db import models, database
from app.db.init_db import create_tables
from app.routers import users

# 🔹 Faqat bitta FastAPI obyekt yaratiladi!
app = FastAPI(
    title="ITicket API",
    version="0.1.0"
)

# 🔹 Ma'lumotlar bazasi jadvallarini yaratish
models.Base.metadata.create_all(bind=database.engine)
create_tables()

# 🔹 Routerlarni ulash
app.include_router(users.router)

# 🔹 CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
