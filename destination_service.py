from typing import List
from app.db.models import Destination
from app.db.repositories.destination_repo import DestinationRepository

class DestinationService:
    def __init__(self, destination_repository: DestinationRepository):
        self.repo = destination_repository

    def create_destination(self, destination_data: dict) -> Destination:
        return self.repo.create_destination(destination_data)

    def get_destination(self, destination_id: int) -> Destination:
        return self.repo.get_destination(destination_id)

    def get_all_destinations(self, skip: int = 0, limit: int = 100) -> List[Destination]:
        return self.repo.get_all_destinations(skip=skip, limit=limit)

    def update_destination(self, destination_id: int, destination_data: dict) -> Destination:
        return self.repo.update_destination(destination_id, destination_data)

    def delete_destination(self, destination_id: int) -> bool:
        return self.repo.delete_destination(destination_id)