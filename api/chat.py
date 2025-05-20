from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from app.services.chat import get_chat_response

router = APIRouter()

@router.post("/")
async def chat(message: Dict[str, Any]) -> Dict[str, str]:
    """Endpoint pour l'API de chat."""
    if not message.get("message"):
        raise HTTPException(status_code=400, detail="Le champ 'message' est requis")
    
    response = await get_chat_response(message["message"])
    return {"response": response or "Aucune réponse disponible"}
