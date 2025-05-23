import httpx
from app.core.config import settings

async def search_hotels(location, check_in, check_out):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{settings.BOOKING_API_URL}/search",
                params={
                    "location": location,
                    "check_in": check_in,
                    "check_out": check_out,
                    "api_key": settings.BOOKING_API_KEY
                }
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise Exception(f"Erreur API: {e.response.status_code}")
        except httpx.RequestError as e:
            raise Exception(f"Erreur de connexion: {str(e)}")