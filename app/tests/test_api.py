from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

VALID_PHOTO = {
    "filename": "test.jpg",
    "url": "https://res.cloudinary.com/demo/image/upload/sample.jpg",
    "category": "nature",
    "width": 1080,
    "height": 1920,
}


def test_get_projects():
    assert client.get("/api/projects").status_code == 200


def test_get_images():
    with patch("app.api.routes.db.fetch_photographs", return_value=[]):
        assert client.get("/api/images").status_code == 200


def test_upload_no_auth():
    assert client.post("/api/upload", json=VALID_PHOTO).status_code == 422


def test_upload_wrong_key():
    assert client.post("/api/upload", json=VALID_PHOTO, headers={"X-API-Key": "wrong"}).status_code == 401


def test_upload_correct_key():
    with patch("app.utils.auth.settings.ADMIN_API_KEY", "test-key"), \
         patch("app.api.routes.db.upload_photo_to_db", return_value=42):
        r = client.post("/api/upload", json=VALID_PHOTO, headers={"X-API-Key": "test-key"})
    assert r.status_code == 201
    assert r.json()["id"] == 42


def test_health_db_up():
    with patch("app.api.routes.db.ping", return_value=True):
        assert client.get("/api/health").status_code == 200


def test_health_db_down():
    with patch("app.api.routes.db.ping", return_value=False):
        assert client.get("/api/health").status_code == 503
