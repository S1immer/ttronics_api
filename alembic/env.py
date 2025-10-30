import asyncio
import os
import sys
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context

# Ensure project root is in sys.path so "import app" works inside container.
# IMPORTANT: append (not insert) so installed top-level packages (like alembic) are not shadowed.
HERE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if HERE not in sys.path:
    sys.path.append(HERE)

config = context.config

# Only call fileConfig if alembic.ini exists
if config.config_file_name and os.path.exists(config.config_file_name):
    fileConfig(config.config_file_name)

# import project metadata (raise clear error if fails)
try:
    from app.db.base import Base  # Base = declarative_base()
    import app.db.models  # noqa: F401 - ensure models are registered on Base
except Exception as e:
    raise RuntimeError(f"Failed to import app package (check PYTHONPATH and that app/ is a package): {e}") from e

DATABASE_URL = os.getenv("DATABASE_URL") or config.get_main_option("sqlalchemy.url")


def run_migrations_offline():
    url = DATABASE_URL
    context.configure(
        url=url,
        target_metadata=Base.metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection):
    context.configure(connection=connection, target_metadata=Base.metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations():
    connectable = create_async_engine(
        DATABASE_URL,
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


def run_migrations_online():
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
