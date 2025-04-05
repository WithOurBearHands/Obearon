"""
Database table related module.
"""

from sqlalchemy import BigInteger
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    """
    Base class needed by SQLAlchemy
    """


class User(Base):
    """
    Table that stores user verification information.
    """

    __tablename__ = "user"

    discord_guild_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    discord_user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    warframe_name: Mapped[str | None] = mapped_column(String(24))
    verification_code: Mapped[int | None]
    verified: Mapped[bool] = mapped_column(default=False, server_default="false")
    linked: Mapped[bool] = mapped_column(default=False, server_default="false")


class GuildRole(Base):
    """
    Table that stores the verify role.
    """

    __tablename__ = "guild_role"

    discord_guild_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    discord_role_id: Mapped[int] = mapped_column(BigInteger)
