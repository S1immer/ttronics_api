import uuid
from sqlalchemy import (
    Column,
    String,
    DateTime,
    Float,
    Integer,
    ForeignKey,
    CheckConstraint,
    Enum as SAEnum,
    func,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship
from enum import Enum

from app.db.base import Base


class DeviceStatus(str, Enum):
    ON = "on"
    OFF = "off"


class Device(Base):
    __tablename__ = "devices"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), unique=True, nullable=False)
    firmware_version = Column(String(64), nullable=True)
    status = Column(SAEnum(DeviceStatus, name="device_status"), nullable=False, default=DeviceStatus.OFF.value)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # relationship to batteries (one-to-many)
    batteries = relationship("Battery", back_populates="device", cascade="all, delete-orphan", passive_deletes=True)


class Battery(Base):
    __tablename__ = "batteries"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    nominal_voltage = Column(Float, nullable=False)  # Volts
    remaining_capacity = Column(Float, nullable=True)  # percent (0..100)
    lifetime = Column(Integer, nullable=True)  # months
    device_id = Column(PG_UUID(as_uuid=True), ForeignKey("devices.id", ondelete="SET NULL"), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    device = relationship("Device", back_populates="batteries")

    __table_args__ = (
        CheckConstraint("remaining_capacity >= 0 AND remaining_capacity <= 100", name="ck_remaining_capacity_range"),
    )
