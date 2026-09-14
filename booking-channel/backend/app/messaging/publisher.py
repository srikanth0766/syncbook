import logging
import pika

from app.core.config import settings
from app.messaging.rabbitmq import get_rabbitmq_connection, BOOKING_REQUEST_QUEUE
from shared.events.booking_events import BookingEvent, BookingEventType

logger = logging.getLogger(__name__)


def publish_booking_request(event: BookingEvent):
    """
    Publishes a BookingEvent to the booking_request_queue.
    Fails gracefully if RabbitMQ is unavailable.
    """
    try:
        connection = get_rabbitmq_connection()
        channel = connection.channel()

        # Idempotently declare queue in case RabbitMQ definitions aren't loaded yet
        channel.queue_declare(queue=BOOKING_REQUEST_QUEUE, durable=True)

        message_body = event.to_json()

        channel.basic_publish(
            exchange="",
            routing_key=BOOKING_REQUEST_QUEUE,
            body=message_body,
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
                content_type="application/json"
            )
        )

        connection.close()
        logger.info(f"Published event {event.event_type} for booking {event.booking_id} to {BOOKING_REQUEST_QUEUE}")
    except Exception as e:
        logger.warning(f"Failed to publish booking request event to RabbitMQ: {e}")


def publish_booking_create_event(booking, channel_id: str = settings.CHANNEL_ID):
    event = BookingEvent(
        event_type=BookingEventType.BOOKING_CREATE_REQUEST,
        channel_id=channel_id,
        booking_id=booking.booking_id,
        payload={
            "booking_id": booking.booking_id,
            "hotel_id": booking.hotel_id,
            "room_type_id": booking.room_type_id,
            "customer_name": booking.customer_name,
            "customer_email": booking.customer_email,
            "check_in_date": str(booking.check_in_date),
            "check_out_date": str(booking.check_out_date),
            "status": booking.status,
            "channel_id": channel_id,
        }
    )
    publish_booking_request(event)
    return event


def publish_booking_update_event(booking, channel_id: str = settings.CHANNEL_ID):
    event = BookingEvent(
        event_type=BookingEventType.BOOKING_UPDATE_REQUEST,
        channel_id=channel_id,
        booking_id=booking.booking_id,
        payload={
            "booking_id": booking.booking_id,
            "hotel_id": booking.hotel_id,
            "room_type_id": booking.room_type_id,
            "customer_name": booking.customer_name,
            "customer_email": booking.customer_email,
            "check_in_date": str(booking.check_in_date),
            "check_out_date": str(booking.check_out_date),
            "status": booking.status,
            "channel_id": channel_id,
        }
    )
    publish_booking_request(event)
    return event


def publish_booking_cancel_event(booking, channel_id: str = settings.CHANNEL_ID):
    event = BookingEvent(
        event_type=BookingEventType.BOOKING_CANCEL_REQUEST,
        channel_id=channel_id,
        booking_id=booking.booking_id,
        payload={
            "booking_id": booking.booking_id,
            "hotel_id": booking.hotel_id,
            "room_type_id": booking.room_type_id,
            "customer_name": booking.customer_name,
            "customer_email": booking.customer_email,
            "status": booking.status,
            "channel_id": channel_id,
        }
    )
    publish_booking_request(event)
    return event
