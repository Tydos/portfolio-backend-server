from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

MOCK_PHOTOS = [
    {"id": 1, "url": "https://example.com/photo1.jpg", "title": "Test Photo", "category": "Landscape"},
]

VALID_PHOTO = {
    "filename": "test.jpg",
    "url": "https://res.cloudinary.com/demo/image/upload/sample.jpg",
    "category": "nature",
    "width": 1080,
    "height": 1920,
}


def test_get_portfolio():
    response = client.get("/api/portfolio")
    assert response.status_code == 200
    body = response.json()
    assert "name" in body
    assert "skills" in body
    assert "projects" in body


def test_get_images():
    with patch("app.api.routes.db.fetch_photographs", return_value=MOCK_PHOTOS):
        response = client.get("/api/images")
    assert response.status_code == 200
    assert response.json()


def test_upload_no_auth():
    response = client.post("/api/upload", json=VALID_PHOTO)
    assert response.status_code == 422


def test_upload_wrong_key():
    response = client.post("/api/upload", json=VALID_PHOTO, headers={"X-API-Key": "wrong"})
    assert response.status_code == 401


def test_upload_correct_key():
    with patch("app.utils.auth.settings.ADMIN_API_KEY", "test-key"), \
         patch("app.api.routes.db.upload_photo_to_db", return_value=42):
        response = client.post("/api/upload", json=VALID_PHOTO, headers={"X-API-Key": "test-key"})
    assert response.status_code == 201
    assert response.json()["id"] == 42


def test_health_db_up():
    with patch("app.api.routes.db.ping", return_value=True):
        response = client.get("/api/health")
    assert response.status_code == 200


def test_health_db_down():
    with patch("app.api.routes.db.ping", return_value=False):
        response = client.get("/api/health")
    assert response.status_code == 503
