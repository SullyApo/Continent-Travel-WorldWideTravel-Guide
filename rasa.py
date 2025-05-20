import httpx
from typing import Union
from app.core.config import settings

async def send_to_rasa(message: str) -> Union[str, None]:
    """Envoie un message au serveur RASA et retourne la réponse."""
    async with httpx.AsyncClient(timeout=5.0) as client:
        try:
            response = await client.post(
                settings.RASA_URL,
                json={"sender": "user", "message": message}
            )
            response.raise_for_status()
            
            if not (data := response.json()):
                return None
                
            return " ".join(d.get("text", "") for d in data) if isinstance(data, list) else str(data)
            
        except httpx.HTTPStatusError as e:
            return f"Erreur HTTP {e.response.status_code}: {str(e)}"
        except httpx.RequestError as e:
            return f"Erreur de connexion: {str(e)}"
        except Exception as e:
            return f"Erreur inattendue: {str(e)}"