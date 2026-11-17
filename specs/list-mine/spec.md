# Spec: List my reservations

Status: active

## Context

Python 3.12, FastAPI, SQLAlchemy 2. Imitate `app/features/create.py` for the response model.
Owns: `app/features/list_mine.py`, `tests/test_list_mine.py`
Uses: `app/models.py`, `app/auth.py` (`X-Diner-Id` header).

## Source

> As a diner, I want to see my reservations so that I know what I have booked and what I cancelled.

## Requirements

- **LIST-01** WHEN a diner sends `GET /reservations`, the API SHALL return 200 with only that diner's reservations, ordered by start time ascending.
- **LIST-02** WHEN the request has `?status=CONFIRMED` or `?status=CANCELLED`, the API SHALL return only reservations with that status.
- **LIST-03** IF `status` is any other value, THEN the API SHALL return 422.
- **LIST-04** IF the diner has no reservations, THEN the API SHALL return 200 and an empty list.

A missing `X-Diner-Id` header returns 401; that behaviour belongs to `app/auth.py`, not to this spec.

## Out of scope

Pagination, free-text search, other diners' reservations, restaurant-side views.

## Verify

`pytest -q tests/test_list_mine.py` then `ruff check .` and `python scripts/check_req_coverage.py`
