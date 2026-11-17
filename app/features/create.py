"""Baseline feature: create a reservation. Already merged; not part of any agent task."""

from datetime import datetime

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.auth import current_diner
from app.db import get_db
from app.models import CONFIRMED, Reservation

router = APIRouter()


class ReservationIn(BaseModel):
    restaurant: str = Field(min_length=1, max_length=120)
    starts_at: datetime
    party_size: int = Field(default=2, ge=1, le=20)


class ReservationOut(BaseModel):
    id: int
    diner_id: str
    restaurant: str
    starts_at: datetime
    party_size: int
    status: str

    model_config = {"from_attributes": True}


@router.post("/reservations", status_code=201, response_model=ReservationOut)
def create_reservation(
    body: ReservationIn,
    diner_id: str = Depends(current_diner),
    db: Session = Depends(get_db),
) -> Reservation:
    reservation = Reservation(
        diner_id=diner_id,
        restaurant=body.restaurant,
        starts_at=body.starts_at,
        party_size=body.party_size,
        status=CONFIRMED,
    )
    db.add(reservation)
    db.commit()
    db.refresh(reservation)
    return reservation
