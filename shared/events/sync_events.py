from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, Optional
import uuid
from pydantic import BaseModel, ConfigDict, Field


class SyncEventType(str, Enum):
    BOOKING_CONFIRMED = "BOOKING_CONFIRMED"
    BOOKING_UPDATED = "BOOKING_UPDATED"
    BOOKING_CANCELLED = "BOOKING_CANCELLED"
    HOTEL_DATA_UPDATED = "HOTEL_DATA_UPDATED"
    AVAILABILITY_UPDATED = "AVAILABILITY_UPDATED"


class SyncEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    event_type: SyncEventType
    channel_id: Optional[str] = None
    booking_id: Optional[str] = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    payload: Dict[str, Any]

    model_config = ConfigDict(from_attributes=True)

    def to_json(self) -> str:
        return self.model_dump_json()

    @classmethod
    def from_json(cls, json_str: str) -> "SyncEvent":
        return cls.model_validate_json(json_str)
