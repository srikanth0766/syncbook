from datetime import date
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.services.availability_service import check_availability
from shared.schemas.booking import AvailabilityResponse

router = APIRouter(prefix="/availability", tags=["Availability"])


@router.get("", response_model=AvailabilityResponse)
def get_availability(
    hotel_id: int = Query(..., description="ID of the hotel"),
    room_type_id: int = Query(..., description="ID of the room type"),
    check_in: date = Query(..., description="Check-in date (YYYY-MM-DD)"),
    check_out: date = Query(..., description="Check-out date (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    if check_in >= check_out:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="check_in date must be strictly before check_out date"
        )
    return check_availability(
        db=db,
        hotel_id=hotel_id,
        room_type_id=room_type_id,
        check_in_date=check_in,
        check_out_date=check_out
    )
