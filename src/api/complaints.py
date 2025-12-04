import time
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from src.schemas.complaint import Complaint
from src.db.base import get_session


router = APIRouter()


@router.post("/complaint")
async def add_complaint(request: Complaint, db=Depends(get_session)):
    print(f"request come as : {request}")
    time.sleep(4)
    return JSONResponse(
        content={"message": "Complaint added successfully"},
        status_code=status.HTTP_201_CREATED,
    )
