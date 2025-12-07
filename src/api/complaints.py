from fastapi import APIRouter, Depends, status, HTTPException
from src.schemas.complaint import ComplaintCreate, Complaint as ComplaintSchema
from src.db.base import get_session
from src.db.models import Complaint
from src.utils import get_checksum


router = APIRouter()


@router.get("/complaints", response_model=list[ComplaintSchema])
async def get_all_complaints(db=Depends(get_session)):
    complaints = db.query(Complaint).all()
    return complaints


@router.get("/complaints/{uuid}", response_model=ComplaintSchema)
async def get_complaint(uuid: str, db=Depends(get_session)):
    complaints = db.query(Complaint).filter(Complaint.uuid == uuid).first()

    if not complaints:
        raise HTTPException(
            detail="No Complaint found",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return complaints


@router.post(
    "/complaints", response_model=ComplaintSchema, status_code=status.HTTP_201_CREATED
)
async def add_complaint(request: ComplaintCreate, db=Depends(get_session)):
    """create new complaint (add complaint to db)"""
    checksum = get_checksum(request.message)
    is_existing = db.query(Complaint).filter(Complaint.checksum == checksum).first()

    if is_existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Complaint already exists"
        )

    db_complaint = Complaint(**request.model_dump())
    db.add(db_complaint)
    db.commit()
    db.refresh(db_complaint)

    return db_complaint


@router.delete("/complaints/{id}")
async def delete_complaint(id: int, db=Depends(get_session)):
    db_complaint = db.query(Complaint).filter(Complaint.id == id).first()

    if not db_complaint:
        raise HTTPException(
            detail="Error deleting complaint",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    db.delete(db_complaint)
    db.commit()

    return ({"message": "Complaint deleted successfully"},)


@router.get("/complaints/status")
async def get_complaint_status():
    return {"message": "Complaint added successfully"}
