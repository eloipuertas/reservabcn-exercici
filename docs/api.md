# API reference

Every endpoint of the API has one section here, with the heading `## METHOD /path`.
All endpoints need the header `X-Diner-Id` (401 if it is missing). Times are naive UTC.
`python scripts/check_dod.py` checks that every route of the app has a section.

## POST /reservations

Create a reservation. Spec: baseline (no spec).

Body: `{"restaurant": "Can Pere", "starts_at": "2026-11-20T21:00:00", "party_size": 2}`
(`party_size` is optional, from 1 to 20, default 2).
Answers 201 with the reservation. Invalid body: 422.

## GET /reservations

List the caller's reservations, earliest first. Spec: `specs/list-mine`.

Query: `status=CONFIRMED` or `status=CANCELLED` (optional, other values give 422).
Answers 200 with a list (empty when there are none).

## DELETE /reservations/{reservation_id}

Cancel one of the caller's reservations. Spec: `specs/cancel`.

Answers 200 with the reservation (status `CANCELLED`). 409 if it starts in less than 2 hours or
is not `CONFIRMED`. 404 if it does not exist or belongs to someone else.
