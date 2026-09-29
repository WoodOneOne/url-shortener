def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_link_created(client):
    response = client.post("/links", json={"url": "https://example.com"})
    assert response.status_code == 201
    assert response.json()["url"] == "https://example.com/"


def test_duplicate_link(client):
    response = client.post("/links", json={"url": "https://example.com"})
    assert response.json()["url"] == response.json()["url"]


def test_bad_link(client):
    response = client.post("/links", json={"url": "example.com"})
    assert response.status_code == 422


def test_unknown(client):
    response = client.get("/123456789")
    assert response.status_code == 404


def test_count(client):
    response = client.post("/links", json={"url": "https://example.com"})
    code = response.json()["code"]
    response = client.get(f"/{code}/stats")
    assert response.json()["count"] == 0

    response = client.get(f"/{code}", follow_redirects=False)
    response = client.get(f"/{code}", follow_redirects=False)
    response = client.get(f"/{code}", follow_redirects=False)

    response = client.get(f"/{code}/stats")
    assert response.status_code == 200
    assert response.json()["count"] == 3


def test_redirect(client):
    response = client.post("/links", json={"url": "https://example.com"})
    code = response.json()["code"]
    response = client.get(f"/{code}", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "https://example.com/"

def test_CI():
    assert 1 == 1