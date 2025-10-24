from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas import venue as schemas
from app.services.venue_service import VenueService
from app.dependencies import get_db, get_admin

router = APIRouter(prefix="/venues", tags=["Venues"])
venue_service = VenueService()


@router.post('/', response_model=schemas.VenueResponse)
def create_venue(
    venue_data: schemas.VenueCreate, 
    admin = Depends(get_admin),
    db: Session = Depends(get_db)
):
    return venue_service.create_venue(venue_data, db)

@router.get('/', response_model=List[schemas.VenueResponse])
def get_venues(db: Session = Depends(get_db)):
    return venue_service.get_venues(db)

