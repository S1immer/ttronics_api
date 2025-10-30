from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from uuid import UUID

from app.db.models import Device, Battery
from app.core.config import settings

MAX = settings.MAX_BATTERIES_PER_DEVICE


async def attach_battery_to_device(session: AsyncSession, device_id: UUID, battery_id: UUID):  # no return annotation
    device = await session.get(Device, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    battery = await session.get(Battery, battery_id)
    if not battery:
        raise HTTPException(status_code=404, detail="Battery not found")

    if battery.device_id == device_id:
        return battery

    q = select(func.count()).select_from(Battery).where(Battery.device_id == device_id)  # type: ignore[arg-type]
    res = await session.execute(q)
    count = res.scalar_one()

    if count >= MAX:
        raise HTTPException(status_code=400, detail=f"Device already has {MAX} batteries")

    battery.device_id = device_id
    session.add(battery)
    await session.commit()
    await session.refresh(battery)
    return battery


async def detach_battery_from_device(session: AsyncSession, device_id: UUID, battery_id: UUID):
    battery = await session.get(Battery, battery_id)
    if not battery or battery.device_id != device_id:
        raise HTTPException(status_code=404, detail="Battery not attached to this device")
    battery.device_id = None
    session.add(battery)
    await session.commit()
    await session.refresh(battery)
    return battery
