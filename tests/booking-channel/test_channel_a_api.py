import os
import sys
from datetime import date, timedelta
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../booking-channel/backend")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# Configure environment for Channel A test
os.environ["CHANNEL_ID"] = "channel-a"
os.environ["CHANNEL_NAME"] = "Channel A"
os.environ["DATABASE_URL"] = "sqlite:///./test_channel_a_api.db"

from app.main import app
from app.database.init_db import init_db


def test_channel_a_api_lifecycle():
    print("\n--- Testing Channel A Local Booking API & Lifecycle ---")
    
    init_db()

    with TestClient(app) as client:
        # 1. Health check
        res = client.get("/health")
        assert res.status_code == 200
        data = res.json()
        assert data["channel_id"] == "channel-a"
        assert data["channel_name"] == "Channel A"
        print("✓ GET /health PASSED (Channel A identified)")

        # 2. GET /hotels
        res = client.get("/hotels")
        assert res.status_code == 200
        hotels = res.json()
        assert len(hotels) >= 1
        assert hotels[0]["name"] == "Hotel A"
        print("✓ GET /hotels PASSED")

        # 3. GET /hotels/{id}/room-types
        res = client.get("/hotels/1/room-types")
        assert res.status_code == 200
        assert len(res.json()) == 3
        print("✓ GET /hotels/1/room-types PASSED")

        # 4. GET /availability
        today = date.today()
        tomorrow = today + timedelta(days=1)
        res = client.get(f"/availability?hotel_id=1&room_type_id=1&check_in={today}&check_out={tomorrow}")
        assert res.status_code == 200
        assert res.json()["available_rooms"] == 10
        print("✓ GET /availability PASSED (10 rooms available)")

        # 5. POST /bookings (Create Booking Request -> PENDING status)
        b_payload = {
            "booking_id": "ch-a-b1",
            "hotel_id": 1,
            "room_type_id": 1,
            "customer_name": "Dave Channel-A",
            "customer_email": "dave@channela.com",
            "check_in_date": str(today),
            "check_out_date": str(tomorrow)
        }
        res = client.post("/bookings", json=b_payload)
        assert res.status_code == 201
        booking = res.json()
        assert booking["booking_id"] == "ch-a-b1"
        assert booking["status"] == "PENDING", f"Expected PENDING status, got {booking['status']}"
        print("✓ POST /bookings PASSED (Created with PENDING status)")

        # 6. Check availability decremented by local PENDING booking
        res_avail = client.get(f"/availability?hotel_id=1&room_type_id=1&check_in={today}&check_out={tomorrow}")
        assert res_avail.json()["available_rooms"] == 9
        print("✓ Local PENDING booking decrements availability to 9 PASSED")

        # 7. GET /bookings/{booking_id}
        res = client.get("/bookings/ch-a-b1")
        assert res.status_code == 200
        assert res.json()["customer_name"] == "Dave Channel-A"
        print("✓ GET /bookings/{id} PASSED")

        # 8. PUT /bookings/{booking_id} (Update Booking Request)
        update_payload = {"customer_name": "Dave Channel-A Updated"}
        res = client.put("/bookings/ch-a-b1", json=update_payload)
        assert res.status_code == 200
        assert res.json()["customer_name"] == "Dave Channel-A Updated"
        assert res.json()["status"] == "UPDATED"
        print("✓ PUT /bookings/{id} PASSED (Status set to UPDATED)")

        # 9. DELETE /bookings/{booking_id} (Cancel Booking Request)
        res = client.delete("/bookings/ch-a-b1")
        assert res.status_code == 200
        assert res.json()["status"] == "CANCELLED"
        print("✓ DELETE /bookings/{id} PASSED (Status set to CANCELLED)")

        # 10. Check availability restored
        res_restored = client.get(f"/availability?hotel_id=1&room_type_id=1&check_in={today}&check_out={tomorrow}")
        assert res_restored.json()["available_rooms"] == 10
        print("✓ Cancellation restores availability to 10 PASSED")

    print("\nALL CHANNEL A API LIFECYCLE TESTS PASSED SUCCESSFULLY!")


if __name__ == "__main__":
    test_channel_a_api_lifecycle()
