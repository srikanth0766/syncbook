from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, Optional
import uuid
from pydantic import BaseModel, ConfigDict, Field


class BookingEventType(str, Enum):
    BOOKING_CREATE_REQUEST = "BOOKING_CREATE_REQUEST"
    BOOKING_UPDATE_REQUEST = "BOOKING_UPDATE_REQUEST"
    BOOKING_CANCEL_REQUEST = "BOOKING_CANCEL_REQUEST"


class BookingEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    event_type: BookingEventType
    channel_id: str
    booking_id: Optional[str] = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    payload: Dict[str, Any]

    model_config = ConfigDict(from_attributes=True)

    def to_json(self) -> str:
        return self.model_dump_json()

    @classmethod
    def from_json(cls, json_str: str) -> "BookingEvent":
        return cls.model_validate_json(json_str)
