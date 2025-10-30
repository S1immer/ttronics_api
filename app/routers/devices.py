from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.schemas.device import DeviceCreate, DeviceRead, DeviceUpdate, DeviceStatus
from app.schemas.battery import BatteryRead
from app.db.models import Device, Battery
from app.db.session import get_async_session

router = APIRouter(prefix="/devices", tags=["devices"])


@router.post(path="/", response_model=DeviceRead, status_code=status.HTTP_201_CREATED)
async def create_device(payload: DeviceCreate, session: AsyncSession = Depends(get_async_session)):
    # store string value for Enum field
    status_val = payload.status.value if payload.status else DeviceStatus.OFF.value
    device = Device(
        name=payload.name,
        firmware_version=payload.firmware_version,
        status=status_val
    )
    session.add(device)
    await session.commit()
    await session.refresh(device)
    return device


@router.get(path="/", response_model=List[DeviceRead])
async def list_devices(session: AsyncSession = Depends(get_async_session)):
    q = select(Device)
    res = await session.execute(q)
    return res.scalars().all()


@router.get(path="/{device_id}", response_model=DeviceRead)
async def get_device(device_id: UUID, session: AsyncSession = Depends(get_async_session)):
    device = await session.get(Device, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device


@router.put(path="/{device_id}", response_model=DeviceRead)
async def update_device(device_id: UUID, payload: DeviceUpdate, session: AsyncSession = Depends(get_async_session)):
    device = await session.get(Device, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    if payload.name is not None:
        device.name = payload.name
    if payload.firmware_version is not None:
        device.firmware_version = payload.firmware_version
    if payload.status is not None:
        device.status = payload.status.value

    session.add(device)
    await session.commit()
    await session.refresh(device)
    return device


@router.delete(path="/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_device(device_id: UUID, session: AsyncSession = Depends(get_async_session)):
    device = await session.get(Device, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    await session.delete(device)
    await session.commit()
    return None


@router.get(path="/{device_id}/batteries", response_model=List[BatteryRead])
async def list_device_batteries(device_id: UUID, session: AsyncSession = Depends(get_async_session)):
    device = await session.get(Device, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    q = select(Battery).where(Battery.device_id == device_id)  # type: ignore[arg-type]
    res = await session.execute(q)
    return res.scalars().all()
