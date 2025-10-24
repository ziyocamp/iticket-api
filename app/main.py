from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import users, venues, events, tickets, orders

app = FastAPI(
    title="ITicket API",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(venues.router)
app.include_router(events.router)
app.include_router(tickets.router)
app.include_router(orders.router)
