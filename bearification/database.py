import os

from sqlalchemy import String
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

async_engine = create_async_engine(
    os.environ["POSTGRES_URL"],
    echo=False,
    pool_size=2,
    max_overflow=4,
)
async_session = async_sessionmaker(
    async_engine, expire_on_commit=False, class_=AsyncSession
)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    discord_id: Mapped[int] = mapped_column(primary_key=True)
    warframe_name: Mapped[str | None] = mapped_column(String(24))
    verification_code: Mapped[int | None]
    verified: Mapped[bool] = mapped_column(default=False, server_default="false")


async def create_database():
    async with async_engine.begin() as session:
        await session.run_sync(User.metadata.create_all)
