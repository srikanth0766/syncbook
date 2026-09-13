import os
import sys
from datetime import date, timedelta

# Add parent directories to sys.path for importing app modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../hotel-pms")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.database.connection import engine, Base, SessionLocal
from app.database.init_db import init_db
from app.services.hotel_service import get_all_hotels, get_hotel_by_id, get_room_types_by_hotel
from app.services.availability_service import check_availability
from app.services.booking_service import create_booking, get_booking_by_id, update_booking, cancel_booking
from shared.schemas.booking import BookingCreate, BookingUpdate, BookingStatus


def test_hotel_pms_database():
    print("Initializing Database & Seed Data...")
    init_db()
    
    db = SessionLocal()
    try:
        # 1. Verify Hotels & Room Types
        hotels = get_all_hotels(db)
        assert len(hotels) >= 1, "Hotel seed failed"
        hotel = get_hotel_by_id(db, 1)
        assert hotel.name == "Hotel A", f"Expected Hotel A, got {hotel.name}"
        
        room_types = get_room_types_by_hotel(db, 1)
        assert len(room_types) == 3, f"Expected 3 room types, got {len(room_types)}"
        
        room_map = {rt.name: rt.total_rooms for rt in room_types}
        assert room_map["Standard Room"] == 10
        assert room_map["Deluxe Room"] == 5
        assert room_map["Suite"] == 2
        print("✓ Hotel & Room Types Seed Verified")
        
        # 2. Check Availability
        today = date.today()
        tomorrow = today + timedelta(days=1)
        
        avail = check_availability(db, hotel_id=1, room_type_id=1, check_in_date=today, check_out_date=tomorrow)
        assert avail.available_rooms == 10
        assert avail.is_available is True
        print("✓ Availability Check Verified")
        
        # 3. Create Booking
        b_create = BookingCreate(
            booking_id="test-booking-1",
            hotel_id=1,
            room_type_id=1,
            customer_name="Alice Smith",
            customer_email="alice@example.com",
            check_in_date=today,
            check_out_date=tomorrow
        )
        booking = create_booking(db, b_create)
        assert booking.booking_id == "test-booking-1"
        assert booking.status == "CONFIRMED"
        print("✓ Create Booking Verified")
        
        # 4. Re-check Availability (should drop from 10 to 9)
        avail_after = check_availability(db, hotel_id=1, room_type_id=1, check_in_date=today, check_out_date=tomorrow)
        assert avail_after.available_rooms == 9
        print("✓ Availability Decremented Verified")
        
        # 5. Update Booking
        b_update = BookingUpdate(customer_name="Alice Johnson")
        updated = update_booking(db, "test-booking-1", b_update)
        assert updated.customer_name == "Alice Johnson"
        print("✓ Update Booking Verified")
        
        # 6. Cancel Booking
        cancelled = cancel_booking(db, "test-booking-1")
        assert cancelled.status == "CANCELLED"
        
        # 7. Check Availability after cancellation (should return to 10)
        avail_final = check_availability(db, hotel_id=1, room_type_id=1, check_in_date=today, check_out_date=tomorrow)
        assert avail_final.available_rooms == 10
        print("✓ Cancel Booking & Availability Restoration Verified")
        
        print("\nALL PMS DATABASE TESTS PASSED SUCCESSFULLY!")
    finally:
        db.close()


if __name__ == "__main__":
    test_hotel_pms_database()
