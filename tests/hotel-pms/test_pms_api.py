import os
import sys
from datetime import date, timedelta
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../hotel-pms")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.main import app
from app.database.init_db import init_db


def test_hotel_pms_api_lifecycle():
    print("\n--- Testing Hotel/PMS API Endpoints ---")
    
    # Explicitly initialize tables and seed data
    init_db()

    with TestClient(app) as client:
        # 1. GET /health
        res = client.get("/health")
        assert res.status_code == 200
        assert res.json()["status"] == "ok"
        print("✓ GET /health PASSED")

        # 2. GET /hotels
        res = client.get("/hotels")
        assert res.status_code == 200
        hotels = res.json()
        assert len(hotels) >= 1
        assert hotels[0]["name"] == "Hotel A"
        print("✓ GET /hotels PASSED")

        # 3. GET /hotels/{hotel_id}
        res = client.get("/hotels/1")
        assert res.status_code == 200
        assert res.json()["name"] == "Hotel A"

        res_404 = client.get("/hotels/9999")
        assert res_404.status_code == 404
        print("✓ GET /hotels/{id} PASSED (200 & 404)")

        # 4. GET /hotels/{hotel_id}/room-types
        res = client.get("/hotels/1/room-types")
        assert res.status_code == 200
        room_types = res.json()
        assert len(room_types) == 3
        room_names = [rt["name"] for rt in room_types]
        assert "Standard Room" in room_names
        assert "Deluxe Room" in room_names
        assert "Suite" in room_names
        print("✓ GET /hotels/{id}/room-types PASSED")

        # 5. GET /availability
        today = date.today()
        tomorrow = today + timedelta(days=1)

        res = client.get(f"/availability?hotel_id=1&room_type_id=1&check_in={today}&check_out={tomorrow}")
        assert res.status_code == 200
        avail_data = res.json()
        assert avail_data["total_rooms"] == 10
        assert avail_data["available_rooms"] == 10
        assert avail_data["is_available"] is True
        print("✓ GET /availability PASSED")

        # 6. POST /bookings (Create Booking)
        booking_payload = {
            "booking_id": "api-test-b1",
            "hotel_id": 1,
            "room_type_id": 1,
            "customer_name": "Carol Danvers",
            "customer_email": "carol@example.com",
            "check_in_date": str(today),
            "check_out_date": str(tomorrow)
        }
        res = client.post("/bookings", json=booking_payload)
        assert res.status_code == 201
        booking = res.json()
        assert booking["booking_id"] == "api-test-b1"
        assert booking["status"] == "CONFIRMED"
        print("✓ POST /bookings PASSED (201 Created)")

        # Check availability decremented
        res_avail = client.get(f"/availability?hotel_id=1&room_type_id=1&check_in={today}&check_out={tomorrow}")
        assert res_avail.json()["available_rooms"] == 9
        print("✓ Post-booking Availability Check PASSED (Decremented to 9)")

        # 7. GET /bookings/{booking_id}
        res = client.get("/bookings/api-test-b1")
        assert res.status_code == 200
        assert res.json()["customer_name"] == "Carol Danvers"
        print("✓ GET /bookings/{id} PASSED")

        # 8. PUT /bookings/{booking_id} (Update Booking)
        update_payload = {"customer_name": "Carol Danvers-Rambeau"}
        res = client.put("/bookings/api-test-b1", json=update_payload)
        assert res.status_code == 200
        assert res.json()["customer_name"] == "Carol Danvers-Rambeau"
        print("✓ PUT /bookings/{id} PASSED")

        # 9. DELETE /bookings/{booking_id} (Cancel Booking)
        res = client.delete("/bookings/api-test-b1")
        assert res.status_code == 200
        assert res.json()["status"] == "CANCELLED"
        print("✓ DELETE /bookings/{id} PASSED (Cancelled)")

        # Check availability restored
        res_avail_after = client.get(f"/availability?hotel_id=1&room_type_id=1&check_in={today}&check_out={tomorrow}")
        assert res_avail_after.json()["available_rooms"] == 10
        print("✓ Post-cancellation Availability Check PASSED (Restored to 10)")

    print("\nALL HOTEL/PMS API ENDPOINT TESTS PASSED SUCCESSFULLY!")


if __name__ == "__main__":
    test_hotel_pms_api_lifecycle()
