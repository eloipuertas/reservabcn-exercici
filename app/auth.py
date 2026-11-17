"""Fake authentication for the course. Shared contract.

The diner is identified by the ``X-Diner-Id`` header. A real system would use tokens.
"""

from fastapi import Header, HTTPException


def current_diner(x_diner_id: str | None = Header(default=None)) -> str:
    """Return the diner id, or answer 401 when the header is missing."""
    if not x_diner_id:
        raise HTTPException(status_code=401, detail="Missing X-Diner-Id header")
    return x_diner_id
