from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.part import Part
from app.dependencies.db import get_db
from app.repositories.part_repository import PartRepository
from app.services.part_service import PartService
from app.schemas.part import PartCreate, PartUpdate

router = APIRouter(prefix="/parts", tags=["Parts"])

def get_service(db: Session = Depends(get_db)):
    repo = PartRepository(db)
    return PartService(repo)


@router.get("/{part_id}")
def get_part(part_id: int, service: PartService = Depends(get_service), db: Session = Depends(get_db)):
    part = db.query(Part).filter(Part.id == part_id).first()

    if not part:
        raise HTTPException(status_code=404, detail="Part not found")

    return service.build_tree(part)


@router.get("/")
def get_parts(service: PartService = Depends(get_service)):
    return service.get_tree()


@router.post("/")
def create_part(data: PartCreate, service: PartService = Depends(get_service)):
    return service.create(data.model_dump())


@router.delete("/{part_id}")
def delete_part(part_id: int, service: PartService = Depends(get_service)):
    service.delete(part_id)
    return {"status": "deleted"}

@router.patch("/{part_id}")
def update_part(
    part_id: int,
    data: PartUpdate,
    service: PartService = Depends(get_service)
):
    return service.update(part_id, data.model_dump(exclude_unset=True))