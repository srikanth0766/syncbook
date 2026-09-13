from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database.connection import Base


class BookingModel(Base):
    __tablename__ = "bookings"

    booking_id = Column(String(255), primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.hotel_id", ondelete="CASCADE"), nullable=False)
    room_type_id = Column(Integer, ForeignKey("room_types.room_type_id", ondelete="CASCADE"), nullable=False)
    channel_id = Column(String(255), ForeignKey("channels.channel_id", ondelete="SET NULL"), nullable=True)
    customer_name = Column(String(255), nullable=False)
    customer_email = Column(String(255), nullable=False)
    check_in_date = Column(Date, nullable=False)
    check_out_date = Column(Date, nullable=False)
    status = Column(String(50), nullable=False, default="CONFIRMED")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    hotel = relationship("HotelModel", back_populates="bookings")
    room_type = relationship("RoomTypeModel", back_populates="bookings")
    channel = relationship("ChannelModel", back_populates="bookings")
