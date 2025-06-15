"""
Verification model.
"""

from sqlalchemy import BigInteger
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from obearon.database.engine import Base


class Verification(Base):
    """
    Table that stores user verification information.
    """

    __tablename__ = "verification"

    discord_guild_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    discord_user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    warframe_name: Mapped[str | None] = mapped_column(String(24))
    verification_code: Mapped[int | None]
    verified: Mapped[bool] = mapped_column(default=False, server_default="false")
