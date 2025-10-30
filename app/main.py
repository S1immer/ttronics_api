from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db.base import Base
from app.db.session import engine
from app.core.config import settings
from app.routers import devices, batteries


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    if settings.DEBUG:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="ttronics - Battery Monitoring", lifespan=lifespan)

app.include_router(devices.router)
app.include_router(batteries.router)
