"""
Guild role model.
"""

from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from obearon.database.engine import Base


class GuildRole(Base):
    """
    Table that stores the verify role.
    """

    __tablename__ = "guild_role"

    guild_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    verified_role_id: Mapped[int | None] = mapped_column(BigInteger)
    friend_role_id: Mapped[int | None] = mapped_column(BigInteger)
    hibernation_role_id: Mapped[int | None] = mapped_column(BigInteger)
