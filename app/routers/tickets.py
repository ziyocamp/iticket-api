from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas import ticket as schemas
from app.services.ticket_service import TicketService
from app.dependencies import get_db, get_admin

router = APIRouter(prefix="/tickets", tags=["Tickets"])
ticket_service = TicketService()


@router.post('/', response_model=schemas.TicketResponse)
def create_ticket(
    ticket_data: schemas.TicketCreate, 
    admin = Depends(get_admin),
    db: Session = Depends(get_db),
):
    return ticket_service.create_ticket(ticket_data, db)

@router.get('/', response_model=List[schemas.TicketResponse])
def get_tickets(
    db: Session = Depends(get_db)
):
    return ticket_service.get_tickets(db)
