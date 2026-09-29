from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_link_created():
    response = client.post("/links", json={"url":"https://example.com"})

    assert response.status_code == 201
    assert response.json()["url"] == "https://example.com/"

def test_bad_link():
    response = client.post("/links", json={"url":"example.com"})

    assert response.status_code == 422
