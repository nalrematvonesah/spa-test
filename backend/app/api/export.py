from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.models.part import Part
from app.services.export_service import generate_excel, generate_pdf

router = APIRouter(prefix="/export", tags=["export"])


def get_root_part(db: Session) -> Part:
    part = db.query(Part).filter(Part.parent_id == None).first()

    if not part:
        raise HTTPException(status_code=404, detail="Root part not found")

    return part


@router.get("/excel")
def export_excel(db: Session = Depends(get_db)):
    part = get_root_part(db)
    file = generate_excel(part)

    return StreamingResponse(
        file,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=parts.xlsx"}
    )


@router.get("/pdf")
def export_pdf(db: Session = Depends(get_db)):
    part = get_root_part(db)
    file = generate_pdf(part)

    return StreamingResponse(
        file,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=parts.pdf"}
    )