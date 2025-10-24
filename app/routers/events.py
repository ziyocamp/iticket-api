from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas import event as schemas
from app.services.event_service import EventService
from app.dependencies import get_db, get_admin

router = APIRouter(prefix="/events", tags=["Events"])
event_service = EventService()


@router.post('/', response_model=schemas.EventResponse)
def create_event(
    event_data: schemas.EventCreate, 
    admin = Depends(get_admin),
    db: Session = Depends(get_db)
):
    return event_service.create_event(event_data, db)

@router.get('/', response_model=List[schemas.EventResponse])
def get_events(
    db: Session = Depends(get_db)
):
    return event_service.get_events(db)


