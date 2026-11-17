# AGENTS.md

Instructions for any coding agent working in this repository. Humans: see README.md.

## Project

ReservaBCN API for a course case. Python 3.12+, FastAPI, SQLAlchemy 2, pytest.
Every feature lives in `app/features/<feature>.py` and has a spec in `specs/<feature>/spec.md`.

## Commands

- Install: `pip install -r requirements.txt`
- Test: `pytest -q`
- Lint: `ruff check .`
- Requirement coverage: `python scripts/check_req_coverage.py`

## How to work

1. Read the spec for your task first: `specs/<feature>/spec.md`. If it says `Status: draft`, stop and ask a human.
2. Write one test per requirement ID (REQ-01, LIST-02, ...). Put the ID in the test name or docstring.
3. Then write the code. Keep the diff small. One task per commit, message starts with the task id.
4. Stop only when `pytest -q`, `ruff check .` and `python scripts/check_req_coverage.py` all pass.
5. Fill in `.github/pull_request_template.md`, then update `progress/progress.md` with what is done and what is next.

## Boundaries

- Write only in the files your spec owns (see `specs/ownership.md`).
- Never edit `specs/`, `.github/`, `.claude/` or this file. Humans own them (see `.github/CODEOWNERS`).
- Shared contracts (`app/models.py`, `app/db.py`, `app/auth.py`, `app/clock.py`, `app/main.py`, `tests/conftest.py`) need their own pull request. If your task needs a change there, stop and say so.
- Do not push, merge, or commit on `main`. A human opens and merges the pull request.
- Do not invent requirements. If the spec is silent or contradictory, list your question in the pull request and stop.

## Style

- Type hints on public functions. Short docstrings. No new dependencies without asking.
- Business rules are named constants with a comment that cites the requirement ID.

## Done when

- All three commands above pass, the PR template is filled in and `progress/progress.md` is updated.
