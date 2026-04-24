from sqlalchemy.orm import Session
from app.models.part import Part


class PartRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_roots(self):
        return self.db.query(Part).filter(Part.parent_id == None).all()

    def get(self, part_id: int):
        return self.db.query(Part).filter(Part.id == part_id).first()

    def get_all(self):
        return self.db.query(Part).all()
    
    def create(self, data: dict):
        part = Part(**data)
        self.db.add(part)
        self.db.commit()
        self.db.refresh(part)
        return part

    def delete(self, part_id: int):
        part = self.get(part_id)
        if part:
            self.db.delete(part)
            self.db.commit()

    def get_by_id(self, part_id):
        return self.db.query(Part).filter(Part.id == part_id).first()

    def update(self, part_id, data):
        part = self.get_by_id(part_id)

        if not part:
            raise Exception("Not found")

        for key, value in data.items():
            setattr(part, key, value)

        self.db.commit()
        self.db.refresh(part)
        return part