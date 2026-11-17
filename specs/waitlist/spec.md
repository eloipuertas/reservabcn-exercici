# Spec: Waitlist

Status: draft
<!-- Stub for Member 4. Not ready for an agent. -->

## Context

Owns: `app/features/waitlist.py`, `tests/test_waitlist.py`

## Source

> As a diner, I want to join a waitlist for a full time slot so that I get a table if someone cancels.

## Requirements

- **WAIT-01** WHEN a diner joins the waitlist for a full slot, the API SHALL store the request in order of arrival. *(to be completed)*

## Questions to resolve before this becomes `active`

- Depends on availability (AVAIL-01) and on cancel (REQ-01): who is notified, and how?
- Is notification in scope or out of scope?

## Out of scope

To be decided.
