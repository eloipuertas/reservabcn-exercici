"""Tests for specs/cancel/spec.md. One or more tests per requirement id."""

from datetime import timedelta

from tests.conftest import NOW


def test_req_01_cancel_with_enough_notice_sets_cancelled(client, make_reservation):
    """REQ-01: own CONFIRMED reservation, at least 2 hours before start -> 200, CANCELLED."""
    reservation_id = make_reservation(starts_at=NOW + timedelta(hours=3))
    response = client.delete(f"/reservations/{reservation_id}", headers={"X-Diner-Id": "ana"})
    assert response.status_code == 200
    assert response.json()["status"] == "CANCELLED"


def test_req_01_exactly_two_hours_is_allowed(client, make_reservation):
    """REQ-01 boundary: exactly 2 hours before start still counts as 'at least 2 hours'."""
    reservation_id = make_reservation(starts_at=NOW + timedelta(hours=2))
    response = client.delete(f"/reservations/{reservation_id}", headers={"X-Diner-Id": "ana"})
    assert response.status_code == 200


def test_req_02_less_than_two_hours_returns_409_and_changes_nothing(client, make_reservation):
    """REQ-02: start less than 2 hours away -> 409, status stays CONFIRMED."""
    reservation_id = make_reservation(starts_at=NOW + timedelta(hours=1, minutes=59))
    response = client.delete(f"/reservations/{reservation_id}", headers={"X-Diner-Id": "ana"})
    assert response.status_code == 409

    listing = client.get("/reservations", headers={"X-Diner-Id": "ana"}).json()
    assert listing[0]["status"] == "CONFIRMED"


def test_req_03_other_diners_reservation_returns_404(client, make_reservation):
    """REQ-03: a reservation that belongs to somebody else -> 404."""
    reservation_id = make_reservation(diner_id="ana", starts_at=NOW + timedelta(hours=5))
    response = client.delete(f"/reservations/{reservation_id}", headers={"X-Diner-Id": "pau"})
    assert response.status_code == 404


def test_req_03_unknown_id_returns_404(client):
    """REQ-03: an id that does not exist looks the same as someone else's."""
    response = client.delete("/reservations/999", headers={"X-Diner-Id": "ana"})
    assert response.status_code == 404


def test_req_04_already_cancelled_returns_409(client, make_reservation):
    """REQ-04: only CONFIRMED reservations can be cancelled."""
    reservation_id = make_reservation(starts_at=NOW + timedelta(hours=5), status="CANCELLED")
    response = client.delete(f"/reservations/{reservation_id}", headers={"X-Diner-Id": "ana"})
    assert response.status_code == 409


def test_cancel_without_header_returns_401(client, make_reservation):
    reservation_id = make_reservation(starts_at=NOW + timedelta(hours=5))
    assert client.delete(f"/reservations/{reservation_id}").status_code == 401
