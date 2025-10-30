from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.schemas.battery import BatteryCreate, BatteryRead, BatteryUpdate
from app.db.models import Battery
from app.services import attach_battery_to_device, detach_battery_from_device
from app.db.session import get_async_session

router = APIRouter(prefix="/batteries", tags=["batteries"])


@router.post(path="/", response_model=BatteryRead, status_code=status.HTTP_201_CREATED)
async def create_battery(payload: BatteryCreate, session: AsyncSession = Depends(get_async_session)):
    b = Battery(
        name=payload.name,
        nominal_voltage=payload.nominal_voltage,
        remaining_capacity=payload.remaining_capacity,
        lifetime=payload.lifetime,
        device_id=payload.device_id
    )
    session.add(b)
    await session.commit()
    await session.refresh(b)
    return b


@router.get(path="/", response_model=List[BatteryRead])
async def list_batteries(session: AsyncSession = Depends(get_async_session)):
    q = select(Battery)
    res = await session.execute(q)
    return res.scalars().all()


@router.get(path="/{battery_id}", response_model=BatteryRead)
async def get_battery(battery_id: UUID, session: AsyncSession = Depends(get_async_session)):
    b = await session.get(Battery, battery_id)
    if not b:
        raise HTTPException(status_code=404, detail="Battery not found")
    return b


@router.put(path="/{battery_id}", response_model=BatteryRead)
async def update_battery(battery_id: UUID, payload: BatteryUpdate, session: AsyncSession = Depends(get_async_session)):
    b = await session.get(Battery, battery_id)
    if not b:
        raise HTTPException(status_code=404, detail="Battery not found")

    if payload.name is not None:
        b.name = payload.name
    if payload.nominal_voltage is not None:
        b.nominal_voltage = payload.nominal_voltage
    if payload.remaining_capacity is not None:
        b.remaining_capacity = payload.remaining_capacity
    if payload.lifetime is not None:
        b.lifetime = payload.lifetime
    if payload.device_id is not None:
        b.device_id = payload.device_id

    session.add(b)
    await session.commit()
    await session.refresh(b)
    return b


@router.delete(path="/{battery_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_battery(battery_id: UUID, session: AsyncSession = Depends(get_async_session)):
    b = await session.get(Battery, battery_id)
    if not b:
        raise HTTPException(status_code=404, detail="Battery not found")
    await session.delete(b)
    await session.commit()
    return None


@router.post(path="/{battery_id}/attach/to/{device_id}", response_model=BatteryRead)
async def attach(battery_id: UUID, device_id: UUID, session: AsyncSession = Depends(get_async_session)):
    return await attach_battery_to_device(session, device_id, battery_id)


@router.post(path="/{battery_id}/detach/from/{device_id}", response_model=BatteryRead)
async def detach(battery_id: UUID, device_id: UUID, session: AsyncSession = Depends(get_async_session)):
    return await detach_battery_from_device(session, device_id, battery_id)
