from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class HotelBase(BaseModel):
    name: str
    location: str


class HotelCreate(HotelBase):
    pass


class HotelUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None


class HotelResponse(HotelBase):
    hotel_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
