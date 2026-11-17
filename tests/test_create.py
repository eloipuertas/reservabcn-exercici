"""Baseline tests for creating reservations and for the fake authentication."""


def test_create_reservation_returns_201_and_confirmed(client):
    response = client.post(
        "/reservations",
        headers={"X-Diner-Id": "ana"},
        json={"restaurant": "Can Pere", "starts_at": "2026-11-13T20:00:00", "party_size": 4},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["status"] == "CONFIRMED"
    assert body["diner_id"] == "ana"
    assert body["party_size"] == 4


def test_missing_diner_header_returns_401(client):
    response = client.post(
        "/reservations",
        json={"restaurant": "Can Pere", "starts_at": "2026-11-13T20:00:00"},
    )
    assert response.status_code == 401
