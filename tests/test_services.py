import pytest
import sys
import httpx
from pathlib import Path
from unittest.mock import AsyncMock, patch
from app.services.rasa import send_to_rasa
from app.utils.helpers import is_valid_message
from app.db.database import SessionLocal

# Configuration des paths (une seule fois)
sys.path.insert(0, str(Path(__file__).parent.parent))

class TestMessageValidation:
    """Tests pour la validation des messages"""
    def test_valid_message(self):
        assert is_valid_message("Normal message") is True
    
    def test_xss_attempt(self):
        assert is_valid_message("<script>alert('XSS')</script>") is False
    
    @pytest.mark.parametrize("message", [
        "",
        "   ",
        None,
        12345,
        {"key": "value"}
    ])
    def test_invalid_inputs(self, message):
        assert is_valid_message(message) is False

class TestRasaIntegration:
    """Tests pour l'intégration avec Rasa"""
    @pytest.mark.asyncio
    async def test_successful_response(self, mocker):
        # Mock configuré avec des réponses réalistes
        mock_response = [
            {"text": "Bonjour !", "confidence": 0.9},
            {"text": "Comment puis-je aider ?", "image": "help.png"}
        ]
        
        mocker.patch(
            "httpx.AsyncClient.post",
            return_value=AsyncMock(
                status_code=200,
                json=AsyncMock(return_value=mock_response)
            )
        )

        response = await send_to_rasa("Salut")
        assert "Bonjour ! Comment puis-je aider ?" in response

    @pytest.mark.asyncio
    async def test_empty_response(self, mocker):
        mocker.patch(
            "httpx.AsyncClient.post",
            return_value=AsyncMock(
                status_code=200,
                json=AsyncMock(return_value=[]))
        )

        response = await send_to_rasa("Empty")
        assert "No response from RASA" in response

    @pytest.mark.asyncio
    async def test_network_failure(self, mocker):
        mocker.patch(
            "httpx.AsyncClient.post",
            side_effect=httpx.RequestError("Erreur réseau")
        )

        response = await send_to_rasa("Hello")
        assert "Request to RASA failed" in response

    @pytest.mark.asyncio
    async def test_invalid_status_code(self, mocker):
        mocker.patch(
            "httpx.AsyncClient.post",
            return_value=AsyncMock(
                status_code=503,
                json=AsyncMock(return_value={"error": "Unavailable"}))
        )

        response = await send_to_rasa("Test")
        assert "Error from RASA" in response

class TestDatabase:
    """Tests de connexion à la base de données"""
    @pytest.mark.asyncio
    async def test_db_connection(self):
        async with SessionLocal() as db:
            result = await db.execute("SELECT 1")
            assert result is not None
            assert result.scalar() == 1

    @pytest.mark.asyncio
    async def test_db_timeout(self, mocker):
        from sqlalchemy.exc import OperationalError
        mocker.patch(
            "app.db.database.SessionLocal.execute",
            side_effect=OperationalError("", "", "timeout") # type: ignore
        )

        with pytest.raises(OperationalError):
            async with SessionLocal() as db:
                await db.execute("SELECT 1")