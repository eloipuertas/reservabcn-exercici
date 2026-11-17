# Spec: Search availability

Status: draft
<!-- Stub for Member 3. Not ready for an agent: finish the requirements, then change the status to active. -->

## Context

Owns: `app/features/availability.py`, `tests/test_availability.py`

## Source

> As a diner, I want to see which time slots a restaurant has free so that I can book one.

## Requirements

- **AVAIL-01** WHEN a diner sends `GET /restaurants/{id}/availability?date=YYYY-MM-DD`, the API SHALL return the free slots for that date. *(to be completed: what is a slot, how many tables, opening hours)*

## Questions to resolve before this becomes `active`

- Slot length and opening hours?
- How is capacity counted: tables or seats?
- Do `CANCELLED` reservations free their slot immediately?

## Out of scope

To be decided.
