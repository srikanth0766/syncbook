import os
import pika

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")

SYNC_EVENTS_EXCHANGE = "sync_events_exchange"
DEAD_LETTER_EXCHANGE = "dead_letter_exchange"

BOOKING_REQUEST_QUEUE = "booking_request_queue"
BOOKING_REQUEST_RETRY_QUEUE = "booking_request_retry_queue"
BOOKING_REQUEST_DLQ = "booking_request_dlq"

CHANNEL_QUEUES = {
    "channel-a": ("channel_a_queue", "channel_a_retry_queue", "channel_a_dlq", "channel_a_retry_rk", "channel_a_dlk"),
    "channel-b": ("channel_b_queue", "channel_b_retry_queue", "channel_b_dlq", "channel_b_retry_rk", "channel_b_dlk"),
    "channel-c": ("channel_c_queue", "channel_c_retry_queue", "channel_c_dlq", "channel_c_retry_rk", "channel_c_dlk"),
}

RETRY_TTL_MS = 5000  # 5 seconds retry delay


def get_rabbitmq_connection(url: str = RABBITMQ_URL) -> pika.BlockingConnection:
    params = pika.URLParameters(url)
    return pika.BlockingConnection(params)


def setup_rabbitmq_infrastructure(channel: pika.adapters.blocking_connection.BlockingChannel):
    """
    Idempotently declares exchanges, queues, retry queues with TTL, DLQs, and bindings.
    """
    # 1. Declare Exchanges
    channel.exchange_declare(exchange=SYNC_EVENTS_EXCHANGE, exchange_type="fanout", durable=True)
    channel.exchange_declare(exchange=DEAD_LETTER_EXCHANGE, exchange_type="direct", durable=True)

    # 2. Declare Booking Request DLQ & Retry Queue
    channel.queue_declare(queue=BOOKING_REQUEST_DLQ, durable=True)
    channel.queue_bind(
        queue=BOOKING_REQUEST_DLQ,
        exchange=DEAD_LETTER_EXCHANGE,
        routing_key="booking_request_dlk"
    )

    channel.queue_declare(
        queue=BOOKING_REQUEST_RETRY_QUEUE,
        durable=True,
        arguments={
            "x-message-ttl": RETRY_TTL_MS,
            "x-dead-letter-exchange": "",
            "x-dead-letter-routing-key": BOOKING_REQUEST_QUEUE
        }
    )
    channel.queue_bind(
        queue=BOOKING_REQUEST_RETRY_QUEUE,
        exchange=DEAD_LETTER_EXCHANGE,
        routing_key="booking_request_retry_rk"
    )

    channel.queue_declare(
        queue=BOOKING_REQUEST_QUEUE,
        durable=True,
        arguments={
            "x-dead-letter-exchange": DEAD_LETTER_EXCHANGE,
            "x-dead-letter-routing-key": "booking_request_retry_rk"
        }
    )

    # 3. Declare Channel Queues, Retry Queues, DLQs & Bindings
    for ch_id, (queue_name, retry_queue_name, dlq_name, retry_rk, dlk_rk) in CHANNEL_QUEUES.items():
        # DLQ
        channel.queue_declare(queue=dlq_name, durable=True)
        channel.queue_bind(queue=dlq_name, exchange=DEAD_LETTER_EXCHANGE, routing_key=dlk_rk)

        # Retry Queue with TTL dead-lettering back to main queue
        channel.queue_declare(
            queue=retry_queue_name,
            durable=True,
            arguments={
                "x-message-ttl": RETRY_TTL_MS,
                "x-dead-letter-exchange": "",
                "x-dead-letter-routing-key": queue_name
            }
        )
        channel.queue_bind(queue=retry_queue_name, exchange=DEAD_LETTER_EXCHANGE, routing_key=retry_rk)

        # Main Queue
        channel.queue_declare(
            queue=queue_name,
            durable=True,
            arguments={
                "x-dead-letter-exchange": DEAD_LETTER_EXCHANGE,
                "x-dead-letter-routing-key": retry_rk
            }
        )
        channel.queue_bind(queue=queue_name, exchange=SYNC_EVENTS_EXCHANGE, routing_key="")
