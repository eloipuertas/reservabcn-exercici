"""Feature: list my reservations. Spec: specs/list-mine/spec.md (LIST-01 to LIST-03)."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import current_diner
from app.db import get_db
from app.features.create import ReservationOut
from app.models import CANCELLED, CONFIRMED, Reservation

router = APIRouter()


@router.get("/reservations", response_model=list[ReservationOut])
def list_my_reservations(
    status: str | None = None,
    diner_id: str = Depends(current_diner),
    db: Session = Depends(get_db),
) -> list[Reservation]:
    # LIST-03: an unknown status value is a client error.
    if status is not None and status not in (CONFIRMED, CANCELLED):
        raise HTTPException(status_code=422, detail="status must be CONFIRMED or CANCELLED")

    # LIST-01: only the caller's reservations, earliest first.
    query = select(Reservation).where(Reservation.diner_id == diner_id)
    # LIST-02: optional status filter.
    if status is not None:
        query = query.where(Reservation.status == status)
    query = query.order_by(Reservation.starts_at.asc(), Reservation.id.asc())

    # LIST-04: no reservations gives an empty list, not an error.
    return list(db.scalars(query))
