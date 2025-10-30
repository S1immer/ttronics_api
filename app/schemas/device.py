from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from enum import Enum

class DeviceStatus(str, Enum):
    ON = "on"
    OFF = "off"

class DeviceBase(BaseModel):
    name: str = Field(..., description="Unique device name")
    firmware_version: Optional[str] = Field(None, description="Firmware version")
    status: Optional[DeviceStatus] = Field(DeviceStatus.OFF, description="Device status: on/off")

class DeviceCreate(DeviceBase):
    pass

class DeviceUpdate(BaseModel):
    name: Optional[str] = None
    firmware_version: Optional[str] = None
    status: Optional[DeviceStatus] = None

class DeviceRead(DeviceBase):
    id: UUID

    class Config:
        orm_mode = True
