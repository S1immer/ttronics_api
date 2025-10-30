from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.ext.asyncio import AsyncEngine

from app.core.config import settings

engine: AsyncEngine = create_async_engine(settings.DATABASE_URL, future=True, echo=False)

AsyncSessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine, expire_on_commit=False, class_=AsyncSession
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency for FastAPI endpoints:
    async with get_async_session() as session: ...
    or in FastAPI use: session: AsyncSession = Depends(get_async_session)
    """
    async with AsyncSessionLocal() as session:
        yield session
