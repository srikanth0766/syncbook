from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class RoomTypeBase(BaseModel):
    hotel_id: int
    name: str
    total_rooms: int


class RoomTypeCreate(RoomTypeBase):
    pass


class RoomTypeUpdate(BaseModel):
    name: Optional[str] = None
    total_rooms: Optional[int] = None


class RoomTypeResponse(RoomTypeBase):
    room_type_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
