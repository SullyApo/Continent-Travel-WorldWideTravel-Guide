from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import Hebergement  # Nous allons créer ce modèle
from app.db.repositories.hebergement_repo import HebergementRepository
from app.services.hebergement_service import HebergementService
from app.core.security import get_current_user
from app.db.models import User
from pydantic import BaseModel

router = APIRouter(prefix="/api/hebergements", tags=["hebergements"])

# Modèles Pydantic
class HebergementBase(BaseModel):
    nom: str
    type_hebergement: str  # (hôtel, auberge, Airbnb...)
    adresse: str
    ville: str
    pays: str
    prix_nuit: float
    capacite: int
    equipements: Optional[str] = None
    note_moyenne: Optional[float] = None
    image_url: Optional[str] = None

class HebergementCreate(HebergementBase):
    pass

class HebergementResponse(HebergementBase):
    id: int

    class Config:
        orm_mode = True

# Initialisation des dépendances
def get_hebergement_service(db: Session = Depends(get_db)) -> HebergementService:
    hebergement_repo = HebergementRepository(db)
    return HebergementService(hebergement_repo)

@router.post("/", response_model=HebergementResponse, status_code=status.HTTP_201_CREATED)
async def create_hebergement(
    hebergement: HebergementCreate,
    service: HebergementService = Depends(get_hebergement_service),
    current_user: User = Depends(get_current_user)
):
    """Crée un nouvel hébergement"""
    try:
        return service.create_hebergement(hebergement.dict())
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/", response_model=List[HebergementResponse])
async def get_all_hebergements(
    ville: Optional[str] = None,
    type_hebergement: Optional[str] = None,
    prix_max: Optional[float] = None,
    skip: int = 0,
    limit: int = 100,
    service: HebergementService = Depends(get_hebergement_service)
):
    """Récupère tous les hébergements avec filtres optionnels"""
    return service.get_all_hebergements(
        ville=ville,
        type_hebergement=type_hebergement,
        prix_max=prix_max,
        skip=skip,
        limit=limit
    )

@router.get("/{hebergement_id}", response_model=HebergementResponse)
async def get_hebergement(
    hebergement_id: int,
    service: HebergementService = Depends(get_hebergement_service)
):
    """Récupère un hébergement spécifique par son ID"""
    hebergement = service.get_hebergement(hebergement_id)
    if not hebergement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hébergement non trouvé"
        )
    return hebergement

@router.put("/{hebergement_id}", response_model=HebergementResponse)
async def update_hebergement(
    hebergement_id: int,
    hebergement: HebergementBase,
    service: HebergementService = Depends(get_hebergement_service),
    current_user: User = Depends(get_current_user)
):
    """Met à jour un hébergement existant"""
    try:
        updated_hebergement = service.update_hebergement(hebergement_id, hebergement.dict())
        if not updated_hebergement:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Hébergement non trouvé"
            )
        return updated_hebergement
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete("/{hebergement_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_hebergement(
    hebergement_id: int,
    service: HebergementService = Depends(get_hebergement_service),
    current_user: User = Depends(get_current_user)
):
    """Supprime un hébergement"""
    success = service.delete_hebergement(hebergement_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hébergement non trouvé"
        )
    return None