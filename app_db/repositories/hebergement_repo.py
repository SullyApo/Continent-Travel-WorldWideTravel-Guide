from sqlalchemy.orm import Session
from app.db.models import Hebergement

class HebergementRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_hebergement(self, hebergement_data: dict):
        hebergement = Hebergement(**hebergement_data)
        self.db.add(hebergement)
        self.db.commit()
        self.db.refresh(hebergement)
        return hebergement

    def get_hebergement(self, hebergement_id: int):
        return self.db.query(Hebergement).filter(Hebergement.id == hebergement_id).first()

    def get_all_hebergements(self, ville=None, type_hebergement=None, prix_max=None, skip=0, limit=100):
        query = self.db.query(Hebergement)
        
        if ville:
            query = query.filter(Hebergement.ville.ilike(f"%{ville}%"))
        if type_hebergement:
            query = query.filter(Hebergement.type_hebergement == type_hebergement)
        if prix_max:
            query = query.filter(Hebergement.prix_nuit <= prix_max)
            
        return query.offset(skip).limit(limit).all()

    def update_hebergement(self, hebergement_id: int, hebergement_data: dict):
        hebergement = self.get_hebergement(hebergement_id)
        if not hebergement:
            return None
        
        for key, value in hebergement_data.items():
            setattr(hebergement, key, value)
        
        self.db.commit()
        self.db.refresh(hebergement)
        return hebergement

    def delete_hebergement(self, hebergement_id: int):
        hebergement = self.get_hebergement(hebergement_id)
        if not hebergement:
            return False
        
        self.db.delete(hebergement)
        self.db.commit()
        return True