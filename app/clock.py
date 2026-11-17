"""Clock dependency. Shared contract: change only through its own PR.

All datetimes in the API are naive UTC. Tests override ``get_now`` to freeze time.
"""

from datetime import UTC, datetime


def get_now() -> datetime:
    """Return the current time as a naive UTC datetime."""
    return datetime.now(UTC).replace(tzinfo=None)
