from sqlalchemy.orm import Session
from app.db.models import Destination

class DestinationRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_destination(self, destination_data: dict):
        destination = Destination(**destination_data)
        self.db.add(destination)
        self.db.commit()
        self.db.refresh(destination)
        return destination

    def get_destination(self, destination_id: int):
        return self.db.query(Destination).filter(Destination.id == destination_id).first()

    def get_all_destinations(self, skip: int = 0, limit: int = 100):
        return self.db.query(Destination).offset(skip).limit(limit).all()

    def update_destination(self, destination_id: int, destination_data: dict):
        destination = self.get_destination(destination_id)
        if not destination:
            return None
        
        for key, value in destination_data.items():
            setattr(destination, key, value)
        
        self.db.commit()
        self.db.refresh(destination)
        return destination

    def delete_destination(self, destination_id: int):
        destination = self.get_destination(destination_id)
        if not destination:
            return False
        
        self.db.delete(destination)
        self.db.commit()
        return True
    
    # backend/app/db/repositories/destination_repo.py
    def get_destination_by_name(self, name: str) -> Optional[Destination]:
        return self.db.query(Destination).filter(Destination.name.ilike(f"%{name}%")).first()