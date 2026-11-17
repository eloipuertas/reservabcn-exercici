"""Shared test fixtures. Shared contract: change only through its own PR."""

from datetime import datetime

import pytest
from fastapi.testclient import TestClient

from app.clock import get_now
from app.db import Base, SessionLocal, engine
from app.main import app
from app.models import CONFIRMED, Reservation

# Frozen "now" used by every test. All start times are expressed relative to it.
NOW = datetime(2026, 11, 12, 12, 0, 0)


@pytest.fixture(autouse=True)
def fresh_database():
    """Start every test with empty tables."""
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    yield


@pytest.fixture
def client():
    app.dependency_overrides[get_now] = lambda: NOW
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def make_reservation():
    """Insert a reservation directly in the database and return its id."""

    def _make(diner_id="ana", starts_at=NOW, status=CONFIRMED, restaurant="Can Pere"):
        with SessionLocal() as db:
            reservation = Reservation(
                diner_id=diner_id,
                restaurant=restaurant,
                starts_at=starts_at,
                party_size=2,
                status=status,
            )
            db.add(reservation)
            db.commit()
            return reservation.id

    return _make
