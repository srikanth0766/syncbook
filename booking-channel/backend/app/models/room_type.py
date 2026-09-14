from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database.connection import Base


class RoomTypeModel(Base):
    __tablename__ = "room_types"

    room_type_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    hotel_id = Column(Integer, ForeignKey("hotels.hotel_id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    total_rooms = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    hotel = relationship("HotelModel", back_populates="room_types")
    bookings = relationship("BookingModel", back_populates="room_type", cascade="all, delete-orphan")
