from pydantic import BaseModel, Field, confloat, conint
from typing import Optional
from uuid import UUID

class BatteryBase(BaseModel):
    name: str = Field(..., description="Battery name")
    nominal_voltage: float = Field(..., description="Nominal voltage (V)")
    remaining_capacity: Optional[confloat(ge=0, le=100)] = Field(None, description="Remaining capacity in % (0-100)")
    lifetime: Optional[conint(ge=0)] = Field(None, description="Lifetime in months")

class BatteryCreate(BatteryBase):
    device_id: Optional[UUID] = None

class BatteryUpdate(BaseModel):
    name: Optional[str] = None
    nominal_voltage: Optional[float] = None
    remaining_capacity: Optional[confloat(ge=0, le=100)] = None
    lifetime: Optional[conint(ge=0)] = None
    device_id: Optional[UUID] = None

class BatteryRead(BatteryBase):
    id: UUID
    device_id: Optional[UUID] = None

    class Config:
        orm_mode = True
