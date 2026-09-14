from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.core.config import settings
from app.api.hotels import router as hotels_router
from app.api.availability import router as availability_router
from app.api.bookings import router as bookings_router
from app.database.init_db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize local channel database tables & seed data on startup
    try:
        init_db()
    except Exception as e:
        print(f"Warning: Channel DB initialization exception: {e}")
    yield


app = FastAPI(
    title=f"Booking Channel Service - {settings.CHANNEL_NAME}",
    description=f"Local Booking Channel API for {settings.CHANNEL_NAME} ({settings.CHANNEL_ID})",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(hotels_router)
app.include_router(availability_router)
app.include_router(bookings_router)


@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "ok",
        "service": "booking-channel",
        "channel_id": settings.CHANNEL_ID,
        "channel_name": settings.CHANNEL_NAME
    }
