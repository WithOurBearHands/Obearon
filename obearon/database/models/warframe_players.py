"""
Warframe player model.
"""

from sqlalchemy import Integer
from sqlalchemy import JSON
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from obearon.database.engine import Base


class WarframePlayers(Base):
    """
    Table that stores player data from guild inventory API.
    """

    __tablename__ = "warframe_players"

    oid: Mapped[str] = mapped_column(String, unique=True, nullable=False, primary_key=True)
    mastery_rank: Mapped[int] = mapped_column(Integer, nullable=False)
    in_clan: Mapped[bool] = mapped_column(default=True, nullable=False)
    blacklisted: Mapped[bool] = mapped_column(default=False, nullable=False)
