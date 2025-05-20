import pytest
from unittest.mock import AsyncMock, patch
from app.services.external.skyscanner import search_flights
from app.services.external.booking import search_hotels
from app.core.config import settings
import httpx

# Configurer les URLs de test
TEST_SKYSCANNER_URL = "https://api.skyscanner.test/v3/flights"
TEST_BOOKING_URL = "https://api.booking.test/v1/hotels"

@pytest.fixture
def mock_apis():
    """Fixture pour mocker les réponses API externes"""
    with patch('httpx.AsyncClient.get') as mock_get:
        yield mock_get

@pytest.mark.asyncio
async def test_skyscanner_api_success(mock_apis):
    """Test de l'API Skyscanner avec réponse valide"""
    # Configurer le mock
    mock_response = {
        "flights": [
            {"id": "FL123", "price": 250, "departure": "2023-12-01"}
        ]
    }
    mock_apis.return_value = AsyncMock(
        status_code=200,
        json=AsyncMock(return_value=mock_response)
    )

    # Appeler la fonction à tester
    result = await search_flights("PARIS", "NEW YORK", "2023-12-01")

    # Vérifications
    assert "flights" in result
    assert len(result["flights"]) > 0
    mock_apis.assert_called_once_with(
        f"{TEST_SKYSCANNER_URL}/search",
        params={
            "origin": "PARIS",
            "destination": "NEW YORK",
            "date": "2023-12-01",
            "apiKey": settings.SKYSCANNER_API_KEY
        }
    )

@pytest.mark.asyncio
async def test_booking_api_failure(mock_apis):
    """Test de gestion des erreurs de l'API Booking"""
    # Configurer le mock pour simuler une erreur
    mock_apis.side_effect = httpx.RequestError("Erreur de connexion")

    # Appeler la fonction et vérifier la gestion d'erreur
    with pytest.raises(httpx.RequestError):
        await search_hotels("Paris", "2023-12-01", "2023-12-10")

@pytest.mark.asyncio
async def test_skyscanner_api_invalid_response(mock_apis):
    """Test avec réponse API invalide"""
    mock_apis.return_value = AsyncMock(
        status_code=200,
        json=AsyncMock(return_value={})  # Réponse vide
    )

    result = await search_flights("PARIS", "LONDON", "2023-12-01")
    assert result == {}

# Test pour vérifier la configuration des URLs
def test_api_urls():
    """Vérifie que les URLs de test sont différentes des URLs réelles"""
    assert settings.SKYSCANNER_API_URL != TEST_SKYSCANNER_URL
    assert settings.BOOKING_API_URL != TEST_BOOKING_URL

@pytest.mark.asyncio
async def test_aviation_stack_service():
    with patch('httpx.AsyncClient.get') as mock_get:
        mock_get.return_value = AsyncMock(
            status_code=200,
            json=AsyncMock(return_value={
                "data": [{
                    "flight_number": "AF123",
                    "departure": {"airport": "CDG"},
                    "arrival": {"airport": "JFK"}
                }]
            })
        )
        
        service = AviationStackService()
        flights = await service.search_flights("CDG", "JFK", "2023-12-01")
        assert len(flights) > 0
        assert flights[0]["flight_number"] == "AF123"