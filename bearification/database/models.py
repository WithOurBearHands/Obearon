"""
Database table related module.
"""
from sqlalchemy import String, BigInteger
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    discord_guild_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    discord_user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    warframe_name: Mapped[str | None] = mapped_column(String(24))
    verification_code: Mapped[int | None]
    verified: Mapped[bool] = mapped_column(default=False, server_default="false")
    linked: Mapped[bool] = mapped_column(default=False, server_default="false")
