from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

DEV_HEADERS = {"Authorization": "Bearer Dev888"}
CHECKER_HEADERS = {"Authorization": "Bearer Checker888"}
TEST_PAYLOAD = {"service": "pytest-service", "incident": "INC-101"}


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_incident_full_lifecycle():
    res_create = client.post("/api/incidents", json=TEST_PAYLOAD, headers=DEV_HEADERS)
    assert res_create.status_code == 201
    assert res_create.json() == {"message": "Incident Reported"}

    res_dup = client.post("/api/incidents", json=TEST_PAYLOAD, headers=DEV_HEADERS)
    assert res_dup.status_code == 409
    assert res_dup.json()["detail"] == "This incident is already reported"

    res_forbidden_post = client.post("/api/incidents", json=TEST_PAYLOAD, headers=CHECKER_HEADERS)
    assert res_forbidden_post.status_code == 403

    res_get = client.get("/api/incidents", params={"service": "pytest-service"})
    assert res_get.status_code == 200
    assert ["pytest-service", "INC-101"] in res_get.json()["incidents"]

    res_forbidden_del = client.request("DELETE", "/api/incidents", json=TEST_PAYLOAD, headers=DEV_HEADERS)
    assert res_forbidden_del.status_code == 403

    res_resolve = client.request("DELETE", "/api/incidents", json=TEST_PAYLOAD, headers=CHECKER_HEADERS)
    assert res_resolve.status_code == 200
    assert res_resolve.json() == {"message": "Incident Resolve"}

    res_not_found = client.request("DELETE", "/api/incidents", json=TEST_PAYLOAD, headers=CHECKER_HEADERS)
    assert res_not_found.status_code == 404
    assert res_not_found.json()["detail"] == "Incident not found"