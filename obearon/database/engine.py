"""
Database engine related module.
"""

from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase

async_engine = create_async_engine("sqlite+aiosqlite:///data/obearon.db")
async_session = async_sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)


class Base(DeclarativeBase):
    """
    Base class needed by SQLAlchemy
    """
