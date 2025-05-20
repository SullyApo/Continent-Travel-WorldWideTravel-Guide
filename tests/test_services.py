import pytest
import sys
from pathlib import Path
from unittest.mock import AsyncMock
from app.services.rasa import send_to_rasa

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.rasa import send_to_rasa
from app.utils.helpers import is_valid_message

def test_message_validation():
    assert is_valid_message("Normal") == True
    assert is_valid_message("<script>alert('XSS')</script>") == False

def test_send_to_rasa(mocker):
    # Votre test ici
    pass

@pytest.mark.asyncio
async def test_send_to_rasa_success(mocker):
    """Teste une réponse réussie de Rasa."""
    # 1. Mock de la réponse HTTP (simule une réponse Rasa valide)
    mock_response = [
        {"text": "Bonjour ! Comment puis-je vous aider ?"},
        {"text": "Voici des destinations..."}
    ]
    mocker.patch(
        "httpx.AsyncClient.post",
        return_value=AsyncMock(
            status_code=200,
            json=AsyncMock(return_value=mock_response)
        )
    )

    # 2. Appel de la fonction à tester
    response = await send_to_rasa("Salut")

    # 3. Vérifications
    assert response == "Bonjour ! Comment puis-je vous aider ? Voici des destinations..."

@pytest.mark.asyncio
async def test_send_to_rasa_failure(mocker):
    """Teste un échec de connexion à Rasa."""
    # 1. Mock d'une erreur HTTP
    mocker.patch(
        "httpx.AsyncClient.post",
        side_effect=httpx.RequestError("Erreur réseau")
    )

    # 2. Appel de la fonction
    response = await send_to_rasa("Hello")

    # 3. Vérification du message d'erreur
    assert "Request to RASA failed" in response