from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.hotels import router as hotels_router
from app.api.availability import router as availability_router
from app.api.bookings import router as bookings_router
from app.database.init_db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB tables and seed data on startup
    try:
        init_db()
    except Exception as e:
        print(f"Warning: Database initialization exception: {e}")
    yield


app = FastAPI(
    title="Hotel PMS Service",
    description="Property Management System (PMS) API for Hotel Management & Inventory",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(hotels_router)
app.include_router(availability_router)
app.include_router(bookings_router)


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "service": "hotel-pms"}
