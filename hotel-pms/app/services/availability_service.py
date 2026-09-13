from datetime import date
from typing import Optional
from sqlalchemy import and_
from sqlalchemy.orm import Session
from app.models.room_type import RoomTypeModel
from app.models.booking import BookingModel
from shared.schemas.booking import AvailabilityResponse


def check_availability(
    db: Session, 
    hotel_id: int, 
    room_type_id: int, 
    check_in_date: date, 
    check_out_date: date,
    exclude_booking_id: Optional[str] = None
) -> AvailabilityResponse:
    room_type = db.query(RoomTypeModel).filter(
        RoomTypeModel.hotel_id == hotel_id,
        RoomTypeModel.room_type_id == room_type_id
    ).first()

    if not room_type:
        return AvailabilityResponse(
            hotel_id=hotel_id,
            room_type_id=room_type_id,
            total_rooms=0,
            available_rooms=0,
            is_available=False
        )

    # Find overlapping bookings that are active
    query = db.query(BookingModel).filter(
        BookingModel.hotel_id == hotel_id,
        BookingModel.room_type_id == room_type_id,
        BookingModel.status.in_(["CONFIRMED", "PENDING", "UPDATED"]),
        and_(
            BookingModel.check_in_date < check_out_date,
            BookingModel.check_out_date > check_in_date
        )
    )

    if exclude_booking_id:
        query = query.filter(BookingModel.booking_id != exclude_booking_id)

    booked_count = query.count()
    available_rooms = max(0, room_type.total_rooms - booked_count)
    is_available = available_rooms > 0

    return AvailabilityResponse(
        hotel_id=hotel_id,
        room_type_id=room_type_id,
        total_rooms=room_type.total_rooms,
        available_rooms=available_rooms,
        is_available=is_available
    )
