from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_chat_endpoint():
    response = client.post("/chat/message", json={"message": "Bonjour"})
    assert response.status_code == 200
    assert "Bonjour" in response.json().get("response", "")

def test_dummy():
    assert 1 + 1 == 2

# Tests pour les nouveaux endpoints
def test_compare_destinations():
    response = client.post(
        "/api/voyages/compare",
        json={"destination1": "Paris", "destination2": "Lyon"}
    )
    assert response.status_code == 200
    assert "Comparaison" in response.json()["summary"]

def test_get_urgences():
    response = client.get("/api/voyages/urgences?destination=paris")
    assert response.status_code == 200
    assert response.json()["phone"] == "112"
