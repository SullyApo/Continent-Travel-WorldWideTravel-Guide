from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_chat_endpoint():
    response = client.post("/chat/message", json={"message": "Bonjour"})
    assert response.status_code == 200
    assert "Bonjour" in response.json().get("response", "")

def test_dummy():
    assert 1 + 1 == 2
