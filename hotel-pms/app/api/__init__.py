from app.api.hotels import router as hotels_router
from app.api.availability import router as availability_router
from app.api.bookings import router as bookings_router

__all__ = ["hotels_router", "availability_router", "bookings_router"]
