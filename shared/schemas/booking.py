from datetime import date, datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr


class BookingStatus(str, Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    UPDATED = "UPDATED"
    CANCELLED = "CANCELLED"
    FAILED = "FAILED"


class BookingBase(BaseModel):
    hotel_id: int
    room_type_id: int
    customer_name: str
    customer_email: EmailStr
    check_in_date: date
    check_out_date: date


class BookingCreate(BookingBase):
    booking_id: Optional[str] = None
    channel_id: Optional[str] = None


class BookingUpdate(BaseModel):
    customer_name: Optional[str] = None
    customer_email: Optional[EmailStr] = None
    check_in_date: Optional[date] = None
    check_out_date: Optional[date] = None
    status: Optional[BookingStatus] = None


class BookingResponse(BookingBase):
    booking_id: str
    status: BookingStatus
    channel_id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class AvailabilityCheck(BaseModel):
    hotel_id: int
    room_type_id: int
    check_in_date: date
    check_out_date: date


class AvailabilityResponse(BaseModel):
    hotel_id: int
    room_type_id: int
    total_rooms: int
    available_rooms: int
    is_available: bool
