from shared.schemas.hotel import HotelBase, HotelCreate, HotelUpdate, HotelResponse
from shared.schemas.room_type import RoomTypeBase, RoomTypeCreate, RoomTypeUpdate, RoomTypeResponse
from shared.schemas.booking import (
    BookingStatus,
    BookingBase,
    BookingCreate,
    BookingUpdate,
    BookingResponse,
    AvailabilityCheck,
    AvailabilityResponse,
)

__all__ = [
    "HotelBase",
    "HotelCreate",
    "HotelUpdate",
    "HotelResponse",
    "RoomTypeBase",
    "RoomTypeCreate",
    "RoomTypeUpdate",
    "RoomTypeResponse",
    "BookingStatus",
    "BookingBase",
    "BookingCreate",
    "BookingUpdate",
    "BookingResponse",
    "AvailabilityCheck",
    "AvailabilityResponse",
]
