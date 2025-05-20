from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
from app.services.chat import get_chat_response
from app.core.security import get_current_user
from app.db.models import User, ChatHistory
from app.db.database import SessionLocal
from sqlalchemy.orm import Session
import uuid

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/message")
async def chat(
    message: Dict[str, Any],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not message.get("message"):
        raise HTTPException(status_code=400, detail="Le champ 'message' est requis")
    
    # Générer ou récupérer un session_id (simplifié ici)
    session_id = str(uuid.uuid4())
    
    # Obtenir la réponse du chatbot
    response = await get_chat_response(message["message"])
    
    # Enregistrer dans l'historique
    db_chat = ChatHistory(
        question=message["message"],
        answer=response,
        user_id=current_user.id,
        session_id=session_id
    )
    db.add(db_chat)
    db.commit()
    
    return {
        "response": response or "Aucune réponse disponible",
        "session_id": session_id
    }
