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

def test_duplicate_link():
    response = client.post("/links", json={"url":"https://example.com"})

    assert response.json()["url"] == response.json()["url"]

def test_bad_link():
    response = client.post("/links", json={"url":"example.com"})

    assert response.status_code == 422

def test_unknown():
    response = client.get("/123456789")
    assert response.status_code == 404

def test_stats():
    response = client.post("/links", json={"url":"https://example.com"})
    code = response.json()["code"]
    response = client.get("/"+code+"/stats")

    assert response.status_code == 200

def test_count():
    response = client.post("/links", json={"url":"https://example.com"})
    code = response.json()["code"]
    response = client.get("/"+code+"/stats")
    assert response.json()["count"] == 0

    response = client.get("/"+code)
    response = client.get("/"+code)
    response = client.get("/"+code)
    
    response = client.get("/"+code+"/stats")
    assert response.json()["count"] == 3

def test_redirect():
    response = client.post("/links", json={"url":"https://example.com"})
    code = response.json()["code"]
    response = client.get("/"+code)

    assert response.json() == "https://example.com/"