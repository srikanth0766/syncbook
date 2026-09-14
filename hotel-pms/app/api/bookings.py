from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.services.booking_service import (
    create_booking,
    get_booking_by_id,
    update_booking,
    cancel_booking,
)
from shared.schemas.booking import BookingCreate, BookingUpdate, BookingResponse

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.post("", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
def create_new_booking(booking_data: BookingCreate, db: Session = Depends(get_db)):
    if booking_data.check_in_date >= booking_data.check_out_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="check_in_date must be strictly before check_out_date"
        )
    try:
        booking = create_booking(db, booking_data)
        return booking
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{booking_id}", response_model=BookingResponse)
def get_booking(booking_id: str, db: Session = Depends(get_db)):
    booking = get_booking_by_id(db, booking_id)
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Booking with ID '{booking_id}' not found"
        )
    return booking


@router.put("/{booking_id}", response_model=BookingResponse)
def update_existing_booking(
    booking_id: str,
    booking_data: BookingUpdate,
    db: Session = Depends(get_db)
):
    try:
        booking = update_booking(db, booking_id, booking_data)
        if not booking:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Booking with ID '{booking_id}' not found"
            )
        return booking
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{booking_id}", response_model=BookingResponse)
def cancel_existing_booking(booking_id: str, db: Session = Depends(get_db)):
    booking = cancel_booking(db, booking_id)
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Booking with ID '{booking_id}' not found"
        )
    return booking
