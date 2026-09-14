import os
import sys
from datetime import date, timedelta
from unittest.mock import patch, MagicMock

# Add parent directories to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../booking-channel/backend")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

os.environ["CHANNEL_ID"] = "channel-a"
os.environ["CHANNEL_NAME"] = "Channel A"
os.environ["DATABASE_URL"] = "sqlite:///./test_publisher.db"

from app.database.connection import Base, engine, SessionLocal
from app.database.init_db import init_db
from app.services.booking_service import (
    create_booking_request,
    update_booking_request,
    cancel_booking_request,
)
from shared.schemas.booking import BookingCreate, BookingUpdate
from shared.events.booking_events import BookingEventType


def test_channel_a_event_publishing():
    print("\n--- Testing Channel A Event Publishing to RabbitMQ ---")

    init_db()
    db = SessionLocal()

    today = date.today()
    tomorrow = today + timedelta(days=1)

    try:
        with patch("app.messaging.publisher.publish_booking_request") as mock_publish:
            # 1. Create Booking Request
            b_create = BookingCreate(
                booking_id="pub-test-b1",
                hotel_id=1,
                room_type_id=1,
                customer_name="Eve Publisher",
                customer_email="eve@channela.com",
                check_in_date=today,
                check_out_date=tomorrow
            )
            created = create_booking_request(db, b_create)
            assert created.status == "PENDING"
            assert mock_publish.called
            event_arg = mock_publish.call_args[0][0]
            assert event_arg.event_type == BookingEventType.BOOKING_CREATE_REQUEST
            assert event_arg.channel_id == "channel-a"
            assert event_arg.booking_id == "pub-test-b1"
            assert event_arg.payload["customer_name"] == "Eve Publisher"
            print("✓ CREATE -> Published BOOKING_CREATE_REQUEST event to booking_request_queue")

            # 2. Update Booking Request
            mock_publish.reset_mock()
            b_update = BookingUpdate(customer_name="Eve Publisher Updated")
            updated = update_booking_request(db, "pub-test-b1", b_update)
            assert updated.status == "UPDATED"
            assert mock_publish.called
            event_arg_up = mock_publish.call_args[0][0]
            assert event_arg_up.event_type == BookingEventType.BOOKING_UPDATE_REQUEST
            assert event_arg_up.booking_id == "pub-test-b1"
            assert event_arg_up.payload["customer_name"] == "Eve Publisher Updated"
            print("✓ UPDATE -> Published BOOKING_UPDATE_REQUEST event to booking_request_queue")

            # 3. Cancel Booking Request
            mock_publish.reset_mock()
            cancelled = cancel_booking_request(db, "pub-test-b1")
            assert cancelled.status == "CANCELLED"
            assert mock_publish.called
            event_arg_can = mock_publish.call_args[0][0]
            assert event_arg_can.event_type == BookingEventType.BOOKING_CANCEL_REQUEST
            assert event_arg_can.booking_id == "pub-test-b1"
            assert event_arg_can.payload["status"] == "CANCELLED"
            print("✓ CANCEL -> Published BOOKING_CANCEL_REQUEST event to booking_request_queue")

        print("\nALL CHANNEL A EVENT PUBLISHING TESTS PASSED SUCCESSFULLY!")
    finally:
        db.close()


if __name__ == "__main__":
    test_channel_a_event_publishing()
