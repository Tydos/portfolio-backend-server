from io import BytesIO
from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_projects():
    assert client.get("/api/projects").status_code == 200


def test_get_images():
    with patch("app.api.routes.db.fetch_photographs", return_value=[]):
        assert client.get("/api/images").status_code == 200


def test_upload_no_auth():
    assert client.post("/api/upload", files=[("file", ("test.jpg", BytesIO(b"img"), "image/jpeg"))]).status_code == 422


def test_upload_wrong_key():
    r = client.post(
        "/api/upload",
        files=[("file", ("test.jpg", BytesIO(b"img"), "image/jpeg"))],
        headers={"X-API-Key": "wrong"},
    )
    assert r.status_code == 401


def test_upload_correct_key():
    mock_upload_result = {"url": "https://res.cloudinary.com/demo/image/upload/sample.jpg", "width": 1080, "height": 1920}
    with patch("app.auth.settings.ADMIN_API_KEY", "test-key"), \
         patch("app.routes._uploader.upload", return_value=mock_upload_result), \
         patch("app.routes.db.filename_exists", return_value=False), \
         patch("app.routes.db.upload_photo_to_db", return_value=42):
        r = client.post(
            "/api/upload",
            files=[("file", ("test.jpg", BytesIO(b"img"), "image/jpeg"))],
            data={"category": "nature"},
            headers={"X-API-Key": "test-key"},
        )
    assert r.status_code == 201
    assert r.json()["photos"][0]["id"] == 42


def test_health_db_up():
    with patch("app.routes.db.ping", return_value=True):
        assert client.get("/api/health").status_code == 200


def test_health_db_down():
    with patch("app.routes.db.ping", return_value=False):
        assert client.get("/api/health").status_code == 503
