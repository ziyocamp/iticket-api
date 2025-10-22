from typing import List

from sqlalchemy.orm import Session

from app.db import models
from app.schemas import venue as schemas


class VenueService:

    def get_venues(self, db: Session) -> List[models.Venue]:
        return db.query(models.Venue).all()
    
    def create_venue(self, venue_data: schemas.VenueCreate, db: Session) -> models.Venue:
        new_venue = models.Venue(name=venue_data.name, lon=venue_data.lon, lat=venue_data.lat)

        db.add(new_venue)
        db.commit()
        db.refresh(new_venue)

        return new_venue
    