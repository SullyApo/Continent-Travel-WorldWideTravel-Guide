from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import Destination
from app.db.repositories.destination_repo import DestinationRepository
from app.services.destination_service import DestinationService
from app.core.security import get_current_user
from app.db.models import User
from pydantic import BaseModel

router = APIRouter(prefix="/api/destinations", tags=["destinations"])

# Modèles Pydantic pour la validation des données
class DestinationBase(BaseModel):
    name: str
    description: Optional[str] = None
    price_range: Optional[str] = None
    country: Optional[str] = None
    climate: Optional[str] = None
    activities: Optional[str] = None
    image_url: Optional[str] = None

class DestinationCreate(DestinationBase):
    pass

class DestinationResponse(DestinationBase):
    id: int

    class Config:
        orm_mode = True

# Initialisation des dépendances
def get_destination_service(db: Session = Depends(get_db)) -> DestinationService:
    destination_repo = DestinationRepository(db)
    return DestinationService(destination_repo)

@router.post("/", response_model=DestinationResponse, status_code=status.HTTP_201_CREATED)
async def create_destination(
    destination: DestinationCreate,
    service: DestinationService = Depends(get_destination_service),
    current_user: User = Depends(get_current_user)
):
    """Crée une nouvelle destination"""
    try:
        return service.create_destination(destination.dict())
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/", response_model=List[DestinationResponse])
async def get_all_destinations(
    skip: int = 0,
    limit: int = 100,
    service: DestinationService = Depends(get_destination_service)
):
    """Récupère toutes les destinations"""
    return service.get_all_destinations(skip=skip, limit=limit)

@router.get("/{destination_id}", response_model=DestinationResponse)
async def get_destination(
    destination_id: int,
    service: DestinationService = Depends(get_destination_service)
):
    """Récupère une destination spécifique par son ID"""
    destination = service.get_destination(destination_id)
    if not destination:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Destination non trouvée"
        )
    return destination

@router.put("/{destination_id}", response_model=DestinationResponse)
async def update_destination(
    destination_id: int,
    destination: DestinationBase,
    service: DestinationService = Depends(get_destination_service),
    current_user: User = Depends(get_current_user)
):
    """Met à jour une destination existante"""
    try:
        updated_destination = service.update_destination(destination_id, destination.dict())
        if not updated_destination:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Destination non trouvée"
            )
        return updated_destination
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete("/{destination_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_destination(
    destination_id: int,
    service: DestinationService = Depends(get_destination_service),
    current_user: User = Depends(get_current_user)
):
    """Supprime une destination"""
    success = service.delete_destination(destination_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Destination non trouvée"
        )
    return None