# Spec: <feature name>

Status: draft
<!-- draft = being written, agents must not implement. active = approved, CI checks coverage. -->

## Context

Language, framework, the files this feature owns, and an existing file to imitate.
Owns: `app/features/<feature>.py`, `tests/test_<feature>.py`

## Source

User story and acceptance criteria this spec came from (link or paste).

## Requirements

Use IDs that are never reused. One trigger and one response per line (EARS style).

- **XXX-01** WHEN <trigger>, the system SHALL <response>.
- **XXX-02** IF <unwanted condition>, THEN the system SHALL <response>.

## Out of scope

What the agent must not add.

## Verify

`pytest -q tests/test_<feature>.py`, `ruff check .`, `python scripts/check_req_coverage.py`
