import os
import pika

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")

SYNC_EVENTS_EXCHANGE = "sync_events_exchange"
DEAD_LETTER_EXCHANGE = "dead_letter_exchange"

BOOKING_REQUEST_QUEUE = "booking_request_queue"
RETRY_TTL_MS = 5000  # 5 seconds retry delay


def get_rabbitmq_connection(url: str = RABBITMQ_URL) -> pika.BlockingConnection:
    params = pika.URLParameters(url)
    return pika.BlockingConnection(params)


def setup_channel_queue_infrastructure(
    channel: pika.adapters.blocking_connection.BlockingChannel,
    channel_id: str,
    queue_name: str
):
    """
    Idempotently sets up specific booking channel queue, retry queue with TTL, and DLQ.
    """
    retry_queue_name = f"{channel_id}_retry_queue"
    dlq_name = f"{channel_id}_dlq"
    retry_rk = f"{channel_id}_retry_rk"
    dlk_key = f"{channel_id}_dlk"

    # Declare exchanges
    channel.exchange_declare(exchange=SYNC_EVENTS_EXCHANGE, exchange_type="fanout", durable=True)
    channel.exchange_declare(exchange=DEAD_LETTER_EXCHANGE, exchange_type="direct", durable=True)

    # Declare DLQ & binding
    channel.queue_declare(queue=dlq_name, durable=True)
    channel.queue_bind(queue=dlq_name, exchange=DEAD_LETTER_EXCHANGE, routing_key=dlk_key)

    # Declare Retry Queue (TTL dead-letters back to main channel queue)
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

    # Declare main channel queue (dead-letters to retry_rk) & bind to sync exchange
    channel.queue_declare(
        queue=queue_name,
        durable=True,
        arguments={
            "x-dead-letter-exchange": DEAD_LETTER_EXCHANGE,
            "x-dead-letter-routing-key": retry_rk
        }
    )
    channel.queue_bind(queue=queue_name, exchange=SYNC_EVENTS_EXCHANGE, routing_key="")
