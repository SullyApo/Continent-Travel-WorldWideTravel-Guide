from typing import List
from app.db.models import Hebergement
from app.db.repositories.hebergement_repo import HebergementRepository

class HebergementService:
    def __init__(self, hebergement_repository: HebergementRepository):
        self.repo = hebergement_repository

    def create_hebergement(self, hebergement_data: dict) -> Hebergement:
        return self.repo.create_hebergement(hebergement_data)

    def get_hebergement(self, hebergement_id: int) -> Hebergement:
        return self.repo.get_hebergement(hebergement_id)

    def get_all_hebergements(
        self,
        ville=None,
        type_hebergement=None,
        prix_max=None,
        skip=0,
        limit=100
    ) -> List[Hebergement]:
        return self.repo.get_all_hebergements(
            ville=ville,
            type_hebergement=type_hebergement,
            prix_max=prix_max,
            skip=skip,
            limit=limit
        )

    def update_hebergement(self, hebergement_id: int, hebergement_data: dict) -> Hebergement:
        return self.repo.update_hebergement(hebergement_id, hebergement_data)

    def delete_hebergement(self, hebergement_id: int) -> bool:
        return self.repo.delete_hebergement(hebergement_id)