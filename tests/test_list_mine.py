"""Tests for specs/list-mine/spec.md. One or more tests per requirement id."""

from datetime import timedelta

from tests.conftest import NOW

HEADERS = {"X-Diner-Id": "ana"}


def test_list_01_returns_only_my_reservations_earliest_first(client, make_reservation):
    """LIST-01: only the caller's reservations, ordered by start time ascending."""
    late = make_reservation(diner_id="ana", starts_at=NOW + timedelta(days=2))
    early = make_reservation(diner_id="ana", starts_at=NOW + timedelta(days=1))
    make_reservation(diner_id="pau", starts_at=NOW + timedelta(days=1))

    response = client.get("/reservations", headers=HEADERS)
    assert response.status_code == 200
    assert [item["id"] for item in response.json()] == [early, late]


def test_list_02_status_filter(client, make_reservation):
    """LIST-02: ?status= keeps only reservations with that status."""
    make_reservation(starts_at=NOW + timedelta(days=1), status="CONFIRMED")
    cancelled = make_reservation(starts_at=NOW + timedelta(days=2), status="CANCELLED")

    response = client.get("/reservations?status=CANCELLED", headers=HEADERS)
    assert [item["id"] for item in response.json()] == [cancelled]


def test_list_03_unknown_status_returns_422(client):
    """LIST-03: a status that is not CONFIRMED or CANCELLED is a client error."""
    response = client.get("/reservations?status=PENDING", headers=HEADERS)
    assert response.status_code == 422


def test_list_04_no_reservations_returns_empty_list(client):
    """LIST-04: nothing to show gives 200 and []."""
    response = client.get("/reservations", headers=HEADERS)
    assert response.status_code == 200
    assert response.json() == []


def test_list_without_header_returns_401(client):
    assert client.get("/reservations").status_code == 401
