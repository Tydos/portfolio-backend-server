from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

MOCK_PHOTOS = [
    {"id": 1, "url": "https://example.com/photo1.jpg", "title": "Test Photo", "category": "Landscape"},
]


def test_get_data():
    response = client.get("/api/data")
    assert response.status_code == 200
    assert response.json()


def test_get_projects():
    response = client.get("/api/projects")
    assert response.status_code == 200
    assert response.json()


def test_get_skills():
    response = client.get("/api/skills")
    assert response.status_code == 200
    assert response.json()


def test_get_photographs():
    response = client.get("/api/photographs")
    assert response.status_code == 200
    assert response.json()


def test_get_images():
    with patch("app.api.routes.db.fetch_photographs", return_value=MOCK_PHOTOS):
        response = client.get("/api/images")
    assert response.status_code == 200
    assert response.json()
