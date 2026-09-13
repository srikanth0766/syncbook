from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, ConfigDict


class ChannelStatus(str, Enum):
    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"
    SYNCING = "SYNCING"


class ChannelBase(BaseModel):
    channel_id: str
    name: str
    status: ChannelStatus = ChannelStatus.ONLINE


class ChannelCreate(ChannelBase):
    pass


class ChannelUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[ChannelStatus] = None


class ChannelResponse(ChannelBase):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
