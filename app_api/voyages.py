# backend/app/api/voyages.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Optional
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.db.models import User, Destination
from app.services.destination_service import DestinationService
from pydantic import BaseModel

router = APIRouter(prefix="/api/voyages", tags=["Voyages"])

# Modèles Pydantic pour la validation
class CompareRequest(BaseModel):
    destination1: str
    destination2: str

class UrgenceResponse(BaseModel):
    phone: str
    embassy: str
    hospital: Optional[str] = None

class ConseilResponse(BaseModel):
    visa: str
    health: str
    currency: str

class RestrictionResponse(BaseModel):
    covid: Optional[str] = None
    visa_required: bool
    other: Optional[str] = None

# Dépendances
def get_destination_service(db: Session = Depends(get_db)) -> DestinationService:
    return DestinationService(DestinationRepository(db))

@router.post("/compare")
async def compare_destinations(
    request: CompareRequest,
    service: DestinationService = Depends(get_destination_service),
    current_user: User = Depends(get_current_user)
) -> Dict[str, str]:
    """
    Compare deux destinations sur des critères clés.
    Exemple de réponse : 
    {"summary": "La Provence est mieux pour la gastronomie, la Bretagne pour les paysages."}
    """
    try:
        dest1 = service.get_destination_by_name(request.destination1)
        dest2 = service.get_destination_by_name(request.destination2)
        
        if not dest1 or not dest2:
            raise HTTPException(status_code=404, detail="Destination non trouvée")

        return {
            "summary": f"Comparaison {dest1.name} vs {dest2.name} :\n"
                       f"- Climat : {dest1.climate} vs {dest2.climate}\n"
                       f"- Prix : {dest1.price_range} vs {dest2.price_range}"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/urgences")
async def get_urgences(
    destination: str,
    db: Session = Depends(get_db)
) -> UrgenceResponse:
    """
    Retourne les contacts d'urgence pour une destination.
    """
    # Mock - À remplacer par une vraie source de données (API externe ou DB)
    urgences_db = {
        "paris": {"phone": "112", "embassy": "N/A (local)", "hospital": "Hôpital Necker"},
        "new york": {"phone": "911", "embassy": "+1 212-606-3600", "hospital": "Mount Sinai"}
    }
    
    infos = urgences_db.get(destination.lower())
    if not infos:
        raise HTTPException(status_code=404, detail="Destination non supportée")

    return UrgenceResponse(**infos)

@router.get("/conseils")
async def get_conseils(
    destination: str,
    db: Session = Depends(get_db)
) -> ConseilResponse:
    """
    Conseils pratiques (visa, santé, monnaie).
    """
    # Mock - À implémenter avec une vraie logique
    return ConseilResponse(
        visa="Non requis pour les séjours < 90 jours",
        health="Vaccins recommandés : Hépatite A",
        currency="Euro (EUR)"
    )

@router.get("/restrictions")
async def get_restrictions(
    destination: str,
    db: Session = Depends(get_db)
) -> RestrictionResponse:
    """
    Restrictions de voyage (COVID, visas, etc.).
    """
    # Mock - À connecter à une API externe (ex: OMS)
    return RestrictionResponse(
        covid="Aucune restriction",
        visa_required=False,
        other="Interdiction des drones en centre-ville"
    )