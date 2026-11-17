"""Feature: cancel a reservation. Spec: specs/cancel/spec.md (REQ-01 to REQ-04)."""

from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth import current_diner
from app.clock import get_now
from app.db import get_db
from app.features.create import ReservationOut
from app.models import CANCELLED, CONFIRMED, Reservation

router = APIRouter()

# Illustrative business rule from the spec (REQ-01 and REQ-02).
MIN_NOTICE = timedelta(hours=2)


@router.delete("/reservations/{reservation_id}", response_model=ReservationOut)
def cancel_reservation(
    reservation_id: int,
    diner_id: str = Depends(current_diner),
    db: Session = Depends(get_db),
    now: datetime = Depends(get_now),
) -> Reservation:
    reservation = db.get(Reservation, reservation_id)

    # REQ-03: someone else's reservation looks the same as a missing one.
    if reservation is None or reservation.diner_id != diner_id:
        raise HTTPException(status_code=404, detail="Reservation not found")

    # REQ-04: only CONFIRMED reservations can be cancelled.
    if reservation.status != CONFIRMED:
        raise HTTPException(status_code=409, detail="Reservation is not CONFIRMED")

    # REQ-02: less than 2 hours before the start, nothing changes.
    if reservation.starts_at - now < MIN_NOTICE:
        raise HTTPException(
            status_code=409, detail="Too late: cancel at least 2 hours before start"
        )

    # REQ-01: cancel.
    reservation.status = CANCELLED
    db.commit()
    db.refresh(reservation)
    return reservation
