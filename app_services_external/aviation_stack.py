import httpx
from typing import Dict, List, Optional
from app.core.config import settings
from app.utils.logging import logger
from datetime import datetime, timedelta
from tenacity import retry, stop_after_attempt, wait_exponential

class AviationStackService:
    def __init__(self):
        self.base_url = settings.AVIATIONSTACK_API_URL
        self.api_key = settings.AVIATIONSTACK_API_KEY

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        before_sleep=lambda retry_state: logger.warning(
            f"Retrying AviationStack... (attempt {retry_state.attempt_number})"
        )
    )  

    async def _make_request(self, endpoint: str, params: Dict) -> Optional[Dict]:
        """Méthode générique pour les requêtes API"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    f"{self.base_url}/{endpoint}",
                    params={"access_key": self.api_key, **params}
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"Erreur AviationStack: {e.response.status_code} - {e.response.text}")
            return None
        except httpx.RequestError as e:
            logger.error(f"Erreur de connexion AviationStack: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Erreur inattendue: {str(e)}")
            return None

    async def search_flights(
        self,
        origin: str,
        destination: str,
        date: str,
        return_date: Optional[str] = None,
        adults: int = 1
    ) -> List[Dict]:
        """
        Recherche des vols avec AviationStack
        Args:
            origin: Code IATA de l'aéroport de départ (ex: 'CDG')
            destination: Code IATA de l'aéroport d'arrivée
            date: Date de départ au format 'YYYY-MM-DD'
            return_date: Optionnel, date de retour
            adults: Nombre de passagers adultes
        Returns:
            Liste de vols disponibles
        """
        params = {
            "dep_iata": origin,
            "arr_iata": destination,
            "flight_date": date,
            "adults": adults
        }
        
        if return_date:
            params["return_date"] = return_date

        data = await self._make_request("flights", params)
        return data.get("data", []) if data else []

    async def get_airport_info(self, iata_code: str) -> Optional[Dict]:
        """Obtenir les informations d'un aéroport"""
        data = await self._make_request("airports", {"iata_code": iata_code})
        return data.get("data", [{}])[0] if data else None

    async def check_flight_status(self, flight_number: str, date: str) -> Optional[Dict]:
        """Vérifier le statut d'un vol spécifique"""
        data = await self._make_request(
            "flight_status",
            {"flight_number": flight_number, "flight_date": date}
        )
        return data.get("data", [{}])[0] if data else None

# Instance singleton pour l'utilisation globale
aviation_stack = AviationStackService()