"""
Database engine related module.
"""
import os

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from bearification.database.models import User

async_engine = create_async_engine(
    os.environ["POSTGRES_URL"],
    echo=False,
    pool_size=2,
    max_overflow=4,
)
async_session = async_sessionmaker(
    async_engine, expire_on_commit=False, class_=AsyncSession
)


async def create_tables() -> None:
    """
    Create the user table.
    """
    async with async_engine.begin() as session:
        await session.run_sync(User.metadata.create_all)
