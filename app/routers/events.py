from typing import List
from uuid import uuid4

from fastapi import APIRouter, Depends, UploadFile, File
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

@router.post('/{event_id}/banner', response_model=schemas.EventResponse)
def upload_banner(
    event_id: int,
    banner: UploadFile = File(),
    admin = Depends(get_admin),
    db: Session = Depends(get_db),
):
    event = event_service.get_event(db, event_id)

    file_path = f'banners/{uuid4()}.jpeg'
    with open(file_path, 'wb') as f:
        f.write(banner.file.read())

    return event_service.add_banner_url(db, event, file_path)


@router.get('/', response_model=List[schemas.EventResponse])
def get_events(
    db: Session = Depends(get_db)
):
    return event_service.get_events(db)


