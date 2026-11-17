# Ownership: who may write where

Split the work by spec, give each spec its own files. Humans own this file.

| Owner (replace with names) | Spec | Branch | Worktree | May write only in |
|----------------------------|------|--------|----------|-------------------|
| Member 1 | `specs/cancel` | `feat/cancel` | `../wt-cancel` | `app/features/cancel.py`, `tests/test_cancel.py` |
| Member 2 | `specs/list-mine` | `feat/list-mine` | `../wt-list-mine` | `app/features/list_mine.py`, `tests/test_list_mine.py` |
| Member 3 | `specs/availability` | `feat/availability` | `../wt-availability` | `app/features/availability.py`, `tests/test_availability.py` |
| Member 4 | `specs/waitlist` | `feat/waitlist` | `../wt-waitlist` | `app/features/waitlist.py`, `tests/test_waitlist.py` |

## Shared contracts

One human owner (the team lead). A change goes in its own small pull request, merged before dependent work continues.

- `app/models.py`, `app/db.py`, `app/auth.py`, `app/clock.py`
- `app/main.py` (only registers routers)
- `tests/conftest.py`
- `app/features/create.py` (baseline feature, already merged)

## Registering a new feature

A new feature module needs one line in `app/main.py`. That is a shared contract: the lead adds the import and `include_router` line in a tiny pull request when the spec becomes `active`, so the feature agent never has to touch `app/main.py`.
