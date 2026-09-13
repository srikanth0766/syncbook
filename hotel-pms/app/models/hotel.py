from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.database.connection import Base


class HotelModel(Base):
    __tablename__ = "hotels"

    hotel_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    location = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    room_types = relationship("RoomTypeModel", back_populates="hotel", cascade="all, delete-orphan")
    bookings = relationship("BookingModel", back_populates="hotel", cascade="all, delete-orphan")
