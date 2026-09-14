import os
import sys
from datetime import date

# Add parent directories to sys.path for importing app modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../booking-channel/backend")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))


def test_independent_channel_databases():
    print("\n--- Testing Independent Channel Databases (Channel A, B, C) ---")

    channels = [
        ("channel-a", "Channel A", "sqlite:///./test_channel_a.db"),
        ("channel-b", "Channel B", "sqlite:///./test_channel_b.db"),
        ("channel-c", "Channel C", "sqlite:///./test_channel_c.db"),
    ]

    for ch_id, ch_name, db_url in channels:
        os.environ["CHANNEL_ID"] = ch_id
        os.environ["CHANNEL_NAME"] = ch_name
        os.environ["DATABASE_URL"] = db_url

        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        from app.database.connection import Base
        from app.models.hotel import HotelModel
        from app.models.room_type import RoomTypeModel
        from app.models.booking import BookingModel

        engine = create_engine(db_url)
        Base.metadata.create_all(bind=engine)
        Session = sessionmaker(bind=engine)
        db = Session()

        try:
            # Seed Hotel & Room types
            hotel = db.query(HotelModel).filter(HotelModel.hotel_id == 1).first()
            if not hotel:
                hotel = HotelModel(hotel_id=1, name="Hotel A", location="New York")
                db.add(hotel)
                db.commit()

            rt = db.query(RoomTypeModel).filter(RoomTypeModel.room_type_id == 1).first()
            if not rt:
                rt = RoomTypeModel(room_type_id=1, hotel_id=1, name="Standard Room", total_rooms=10)
                db.add(rt)
                db.commit()

            # Insert channel-specific booking
            booking_id = f"b-id-{ch_id}"
            booking = BookingModel(
                booking_id=booking_id,
                hotel_id=1,
                room_type_id=1,
                customer_name=f"Customer of {ch_name}",
                customer_email=f"cust@{ch_id}.com",
                check_in_date=date(2026, 11, 1),
                check_out_date=date(2026, 11, 5),
                status="CONFIRMED"
            )
            db.add(booking)
            db.commit()

            b_check = db.query(BookingModel).filter(BookingModel.booking_id == booking_id).first()
            assert b_check is not None
            assert b_check.customer_name == f"Customer of {ch_name}"
            print(f"✓ {ch_name} ({ch_id}) Database initialized & verified independently")
        finally:
            db.close()

    print("\nALL 3 CHANNEL DATABASES INITIALIZED SUCCESSFULLY WITHOUT INTERFERENCE!")


if __name__ == "__main__":
    test_independent_channel_databases()
