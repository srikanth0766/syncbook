from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.services.hotel_service import get_all_hotels, get_hotel_by_id, get_room_types_by_hotel
from shared.schemas.hotel import HotelResponse
from shared.schemas.room_type import RoomTypeResponse

router = APIRouter(prefix="/hotels", tags=["Hotels"])


@router.get("", response_model=List[HotelResponse])
def list_hotels(db: Session = Depends(get_db)):
    return get_all_hotels(db)


@router.get("/{hotel_id}", response_model=HotelResponse)
def get_hotel(hotel_id: int, db: Session = Depends(get_db)):
    hotel = get_hotel_by_id(db, hotel_id)
    if not hotel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hotel with ID {hotel_id} not found"
        )
    return hotel


@router.get("/{hotel_id}/room-types", response_model=List[RoomTypeResponse])
def get_hotel_room_types(hotel_id: int, db: Session = Depends(get_db)):
    hotel = get_hotel_by_id(db, hotel_id)
    if not hotel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hotel with ID {hotel_id} not found"
        )
    return get_room_types_by_hotel(db, hotel_id)
