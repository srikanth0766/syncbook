import uuid
from typing import List, Optional
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.booking import BookingModel
from app.services.availability_service import check_availability
from shared.schemas.booking import BookingCreate, BookingUpdate, BookingStatus


def create_booking_request(db: Session, booking_data: BookingCreate) -> BookingModel:
    avail = check_availability(
        db=db,
        hotel_id=booking_data.hotel_id,
        room_type_id=booking_data.room_type_id,
        check_in_date=booking_data.check_in_date,
        check_out_date=booking_data.check_out_date
    )

    if not avail.is_available:
        raise ValueError("No rooms available for the selected dates.")

    booking_id = booking_data.booking_id or str(uuid.uuid4())

    # New bookings are stored locally with status PENDING
    booking = BookingModel(
        booking_id=booking_id,
        hotel_id=booking_data.hotel_id,
        room_type_id=booking_data.room_type_id,
        customer_name=booking_data.customer_name,
        customer_email=str(booking_data.customer_email),
        check_in_date=booking_data.check_in_date,
        check_out_date=booking_data.check_out_date,
        status=BookingStatus.PENDING.value
    )

    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


def get_booking_by_id(db: Session, booking_id: str) -> Optional[BookingModel]:
    return db.query(BookingModel).filter(BookingModel.booking_id == booking_id).first()


def get_all_bookings(db: Session) -> List[BookingModel]:
    return db.query(BookingModel).all()


def update_booking_request(db: Session, booking_id: str, booking_data: BookingUpdate) -> Optional[BookingModel]:
    booking = get_booking_by_id(db, booking_id)
    if not booking:
        return None

    new_check_in = booking_data.check_in_date or booking.check_in_date
    new_check_out = booking_data.check_out_date or booking.check_out_date

    if booking_data.check_in_date or booking_data.check_out_date:
        avail = check_availability(
            db=db,
            hotel_id=booking.hotel_id,
            room_type_id=booking.room_type_id,
            check_in_date=new_check_in,
            check_out_date=new_check_out,
            exclude_booking_id=booking_id
        )
        if not avail.is_available:
            raise ValueError("No rooms available for the updated dates.")

    if booking_data.customer_name is not None:
        booking.customer_name = booking_data.customer_name
    if booking_data.customer_email is not None:
        booking.customer_email = str(booking_data.customer_email)
    if booking_data.check_in_date is not None:
        booking.check_in_date = booking_data.check_in_date
    if booking_data.check_out_date is not None:
        booking.check_out_date = booking_data.check_out_date
    
    # If status specified, update it; otherwise mark as UPDATED
    if booking_data.status is not None:
        booking.status = booking_data.status.value if isinstance(booking_data.status, BookingStatus) else str(booking_data.status)
    else:
        booking.status = BookingStatus.UPDATED.value

    db.commit()
    db.refresh(booking)
    return booking


def cancel_booking_request(db: Session, booking_id: str) -> Optional[BookingModel]:
    booking = get_booking_by_id(db, booking_id)
    if not booking:
        return None

    booking.status = BookingStatus.CANCELLED.value
    db.commit()
    db.refresh(booking)
    return booking
