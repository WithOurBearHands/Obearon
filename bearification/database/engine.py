"""
Database engine related module.
"""

import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

from bearification.database.models import GuildRole
from bearification.database.models import User

load_dotenv()

async_engine = create_async_engine(
    os.environ["POSTGRES_URL"],
    echo=False,
    pool_size=2,
    max_overflow=4,
)
async_session = async_sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)


async def create_tables() -> None:
    """
    Create the user table.
    """
    async with async_engine.begin() as session:
        await session.run_sync(GuildRole.metadata.drop_all)
        await session.run_sync(GuildRole.metadata.create_all)
        await session.run_sync(User.metadata.create_all)
