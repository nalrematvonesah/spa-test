from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.services.export_service import generate_excel, generate_pdf
from app.services.part_service import PartService
from app.repositories.part_repository import PartRepository

router = APIRouter(prefix="/export", tags=["export"])


def get_tree(db: Session):
    repo = PartRepository(db)
    service = PartService(repo)
    return service.get_tree()


@router.get("/excel")
def export_excel(db: Session = Depends(get_db)):
    tree = get_tree(db)
    file = generate_excel(tree)

    return StreamingResponse(
        file,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=parts.xlsx"}
    )


@router.get("/pdf")
def export_pdf(db: Session = Depends(get_db)):
    tree = get_tree(db)
    file = generate_pdf(tree)

    return StreamingResponse(
        file,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=parts.pdf"}
    )