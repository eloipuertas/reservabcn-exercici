# Spec: Cancel a reservation

Status: active

## Context

Python 3.12, FastAPI, SQLAlchemy 2. Imitate `app/features/list_mine.py` for structure.
Owns: `app/features/cancel.py`, `tests/test_cancel.py`
Uses: `app/models.py` (`Reservation`, status `CONFIRMED` or `CANCELLED`), `app/auth.py` (`X-Diner-Id` header), `app/clock.py` (`get_now`, frozen in tests).

## Source

> As a diner, I want to cancel my reservation so that the restaurant can free the table.
> AC: a confirmed reservation can be cancelled, but not less than 2 hours before it starts.

The 2-hour rule and the status codes are illustrative values for the course.

## Requirements

- **REQ-01** WHEN a diner sends `DELETE /reservations/{id}` for their own `CONFIRMED` reservation at least 2 hours before it starts, the API SHALL set `status=CANCELLED` and return 200 with the reservation.
- **REQ-02** IF the reservation starts in less than 2 hours, THEN the API SHALL return 409 and change nothing.
- **REQ-03** IF the reservation does not exist or belongs to another diner, THEN the API SHALL return 404 (the same answer in both cases).
- **REQ-04** IF the reservation is not `CONFIRMED`, THEN the API SHALL return 409 and change nothing.

Added during the clarify step: REQ-04 closes the question "what happens if I cancel twice?".
Exactly 2 hours before the start counts as "at least 2 hours" (REQ-01).

## Out of scope

Refunds, e-mail or push notifications, cancelling on behalf of a diner (admin), restoring a cancelled reservation.

## Verify

`pytest -q tests/test_cancel.py` then `ruff check .` and `python scripts/check_req_coverage.py`
