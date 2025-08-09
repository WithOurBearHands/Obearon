"""
Warframe player names model.
"""

from sqlalchemy import Integer
from sqlalchemy import JSON
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from obearon.database.engine import Base


class WarframePlayerNames(Base):
    """
    Table that stores player names and platform from guild inventory API.
    """

    __tablename__ = "warframe_player_names"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    oid: Mapped[str] = mapped_column(String, ForeignKey("warframe_players.oid"), nullable=False)
    name: Mapped[str] = mapped_column(JSON, nullable=False)
    platform: Mapped[str] = mapped_column(JSON, nullable=False, default="unknown")
