from datetime import datetime

from pydantic import BaseModel, Field


class EventBase(BaseModel):
    name: str
    description: str
    limit_age: int = Field(ge=0)
    venue_id: int
    start_time: datetime
    end_time: datetime


class EventCreate(EventBase):
    pass


class EventResponse(EventBase):
    id: int
    banner: str | None = None

    class Config:
        from_attributes = True
