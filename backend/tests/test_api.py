from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_lists_shillong():
    response = client.get("/api/health")
    assert response.status_code == 200
    body = response.json()
    assert body["destinations"] == ["shillong"]


def test_destinations_endpoint_shape():
    response = client.get("/api/destinations")
    assert response.status_code == 200
    names = {entry["name"] for entry in response.json()["destinations"]}
    assert names == {"Shillong"}


def test_plan_endpoint_returns_itinerary_for_shillong():
    response = client.post("/api/plan", json={
        "origin_city": "Guwahati", "destination": "Shillong", "start_date": "2026-11-10",
        "end_date": "2026-11-12", "travelers": 2, "traveller_type": "friends", "budget": 12000,
        "currency": "INR", "pace": "balanced", "interests": ["outdoors"], "enhance_with_ai": False,
    })
    assert response.status_code == 200
    body = response.json()
    assert body["destination"] == "Shillong"
    assert len(body["days"]) > 0


def test_plan_endpoint_rejects_unsupported_destination():
    response = client.post("/api/plan", json={
        "origin_city": "Delhi", "destination": "Goa", "start_date": "2026-11-10",
        "end_date": "2026-11-12", "enhance_with_ai": False,
    })
    assert response.status_code == 422
