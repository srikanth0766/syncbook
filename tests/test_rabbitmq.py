import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../syncbook")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../booking-channel/backend")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def test_rabbitmq_definitions():
    print("\n--- Testing RabbitMQ Infrastructure & Retry Mechanism ---")

    defs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../rabbitmq/definitions.json"))
    assert os.path.exists(defs_path), f"definitions.json not found at {defs_path}"

    with open(defs_path, "r") as f:
        data = json.load(f)

    # 1. Verify Exchanges
    exchanges = {ex["name"]: ex for ex in data.get("exchanges", [])}
    assert "sync_events_exchange" in exchanges
    assert exchanges["sync_events_exchange"]["type"] == "fanout"
    assert "dead_letter_exchange" in exchanges
    assert exchanges["dead_letter_exchange"]["type"] == "direct"
    print("✓ Exchanges Verified (sync_events_exchange [fanout], dead_letter_exchange [direct])")

    # 2. Verify Main Queues, Retry Queues & DLQs
    queues = {q["name"]: q for q in data.get("queues", [])}
    expected_queues = [
        "booking_request_queue",
        "booking_request_retry_queue",
        "booking_request_dlq",
        "channel_a_queue",
        "channel_a_retry_queue",
        "channel_a_dlq",
        "channel_b_queue",
        "channel_b_retry_queue",
        "channel_b_dlq",
        "channel_c_queue",
        "channel_c_retry_queue",
        "channel_c_dlq"
    ]
    for q_name in expected_queues:
        assert q_name in queues, f"Queue '{q_name}' missing from definitions.json"
    
    # Check Dead-Letter Routing on main queues to retry queues
    assert queues["booking_request_queue"]["arguments"]["x-dead-letter-exchange"] == "dead_letter_exchange"
    assert queues["booking_request_queue"]["arguments"]["x-dead-letter-routing-key"] == "booking_request_retry_rk"

    assert queues["channel_a_queue"]["arguments"]["x-dead-letter-exchange"] == "dead_letter_exchange"
    assert queues["channel_a_queue"]["arguments"]["x-dead-letter-routing-key"] == "channel_a_retry_rk"
    print("✓ Main Queues configured to dead-letter to Retry Keys")

    # Check Retry Queues TTL and routing back to main queues
    assert queues["booking_request_retry_queue"]["arguments"]["x-message-ttl"] == 5000
    assert queues["booking_request_retry_queue"]["arguments"]["x-dead-letter-routing-key"] == "booking_request_queue"

    assert queues["channel_a_retry_queue"]["arguments"]["x-message-ttl"] == 5000
    assert queues["channel_a_retry_queue"]["arguments"]["x-dead-letter-routing-key"] == "channel_a_queue"
    print("✓ Retry Queues configured with 5000ms TTL & routing back to main queues")

    # 3. Verify Bindings
    bindings = data.get("bindings", [])
    dlx_bindings = [b for b in bindings if b["source"] == "dead_letter_exchange"]
    
    retry_bindings = [b for b in dlx_bindings if "retry_queue" in b["destination"]]
    assert len(retry_bindings) == 4, f"Expected 4 retry queue bindings, found {len(retry_bindings)}"

    dlq_bindings = [b for b in dlx_bindings if "dlq" in b["destination"]]
    assert len(dlq_bindings) == 4, f"Expected 4 DLQ bindings, found {len(dlq_bindings)}"
    print("✓ DLX Bindings to Retry Queues and DLQs Verified")

    print("\nALL RABBITMQ RETRY & INFRASTRUCTURE TESTS PASSED SUCCESSFULLY!")


if __name__ == "__main__":
    test_rabbitmq_definitions()
