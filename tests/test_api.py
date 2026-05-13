import os

os.environ.setdefault("DATABASE_URL", "sqlite:///./test.db")
os.environ.setdefault("ENABLE_LEGACY_ROUTES", "true")

from fastapi.testclient import TestClient
from app.main import app
from app.db.session import Base, engine


def setup_module(module):
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def teardown_module(module):
    Base.metadata.drop_all(bind=engine)


def test_v1_crud_and_energy_usage():
    with TestClient(app) as client:
        payload = {"id": "dev-1", "name": "Living Room Light", "type": "Light", "brightness": 88}
        resp = client.post("/api/v1/devices", json=payload)
        assert resp.status_code == 201
        data = resp.json()
        assert data["id"] == "dev-1"
        assert data["type"] == "Light"

        resp = client.get("/api/v1/devices/dev-1")
        assert resp.status_code == 200

        resp = client.put("/api/v1/devices/dev-1/commands/on")
        assert resp.status_code == 200
        assert resp.json()["status"] == "on"

        resp = client.get("/api/v1/energy-usage")
        assert resp.status_code == 200
        assert "total_energy_usage" in resp.json()

        resp = client.delete("/api/v1/devices/dev-1")
        assert resp.status_code == 200


def test_legacy_routes_compatibility():
    with TestClient(app) as client:
        payload = {"id": "legacy-1", "name": "Legacy Cam", "type": "Camera", "resolution": "4k"}
        resp = client.post("/add_device", json=payload)
        assert resp.status_code == 201

        resp = client.get("/devices/legacy-1")
        assert resp.status_code == 200
        assert resp.json()["type"] == "Camera"

        resp = client.get("/devices/legacy-1/on")
        assert resp.status_code == 200
        assert resp.json()["status"] == "on"

        resp = client.get("/energy_usage")
        assert resp.status_code == 200
        assert "total_energy_usage" in resp.json()

        resp = client.delete("/devices/legacy-1")
        assert resp.status_code == 200
