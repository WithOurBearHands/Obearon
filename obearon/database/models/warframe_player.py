"""
Warframe player model.
"""

from sqlalchemy import BigInteger, Integer, String, JSON
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from obearon.database.engine import Base


class WarframePlayer(Base):
    """
    Table that stores player data from guild inventory API.
    """

    __tablename__ = "warframe_player"

    oid: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(24))
    platform_names: Mapped[list[str]] = mapped_column(JSON)
    mastery_rank: Mapped[int] = mapped_column(Integer)
