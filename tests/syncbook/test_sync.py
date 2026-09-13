import os
import sys

# Add parent directories to sys.path for importing app modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../syncbook")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.database.connection import engine, Base, SessionLocal
from app.database.init_db import init_db
from app.models.channel import ChannelModel
from app.models.hotel import HotelModel
from app.models.room_type import RoomTypeModel
from app.models.booking import BookingModel


from datetime import date

def test_syncbook_database():
    print("Initializing Syncbook Database & Seed Data...")
    init_db()

    db = SessionLocal()
    try:
        # Verify Channels
        channels = db.query(ChannelModel).all()
        assert len(channels) == 3, f"Expected 3 channels, got {len(channels)}"
        channel_ids = [ch.channel_id for ch in channels]
        assert "channel-a" in channel_ids
        assert "channel-b" in channel_ids
        assert "channel-c" in channel_ids
        print("✓ Syncbook Channels Seed Verified")

        # Verify Table creation by adding a test hotel & booking
        hotel = db.query(HotelModel).filter(HotelModel.hotel_id == 1).first()
        if not hotel:
            hotel = HotelModel(hotel_id=1, name="Syncbook Central Hotel", location="Central")
            db.add(hotel)
            db.commit()

        rt = db.query(RoomTypeModel).filter(RoomTypeModel.room_type_id == 1).first()
        if not rt:
            rt = RoomTypeModel(room_type_id=1, hotel_id=1, name="Central Suite", total_rooms=5)
            db.add(rt)
            db.commit()

        booking = BookingModel(
            booking_id="sync-test-booking-1",
            hotel_id=1,
            room_type_id=1,
            channel_id="channel-a",
            customer_name="Bob Central",
            customer_email="bob@example.com",
            check_in_date=date(2026, 10, 1),
            check_out_date=date(2026, 10, 5),
            status="CONFIRMED"
        )
        db.add(booking)
        db.commit()

        retrieved_booking = db.query(BookingModel).filter(BookingModel.booking_id == "sync-test-booking-1").first()
        assert retrieved_booking is not None
        assert retrieved_booking.channel_id == "channel-a"
        print("✓ Syncbook Hotel, RoomType & Booking Persistence Verified")

        print("\nALL SYNCBOOK DATABASE TESTS PASSED SUCCESSFULLY!")
    finally:
        db.close()


if __name__ == "__main__":
    test_syncbook_database()
